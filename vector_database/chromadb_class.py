import os
import uuid
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from embedding.model import openai_embedding_model
from utils.preprocess_data import get_data_loader
import time
from utils._hash import get_existing_hashes, compute_hash

class ChromaDB:
    def __init__(self, persist_path="chroma_db", batch=5):
        self.persist_path = persist_path
        self.batch = batch
        self.embedding = openai_embedding_model()

        if os.path.exists(persist_path):
            print("[INFO] Found existing Chroma DB. Loading it...")
        else:
            print("[INFO] Creating new Chroma DB...")

        self.vector_store = Chroma(
            collection_name="chroma_db_collection",
            persist_directory=persist_path,
            embedding_function=self.embedding
        )

    def add(self, docs: list):
        if not docs:
            raise ValueError("Documents list is empty or None.")
        
        existing_docs_in_vectorstore = get_existing_hashes()

        skipped = 0
        added = 0

        print("[INFO] Adding documents...")
        start_time = time.time()

        total = len(docs)

        for i in range(0, total, self.batch):
            batch_docs = docs[i:i + self.batch]


            docs_to_add = []

            for doc in batch_docs:
                doc_hash = compute_hash(doc.page_content)

                if doc_hash in existing_docs_in_vectorstore:
                    skipped += 1
                    continue

                docs_to_add.append(doc)
            

            if docs_to_add:

                batch_ids = [str(uuid.uuid4()) for _ in range(len(docs_to_add))]

                self.vector_store.add_documents(
                    documents=docs_to_add,
                    ids=batch_ids
                )

                added += len(docs_to_add)

                print("-" * 50)
                print(f"☛ Docs added {added}/{total} (skipped: {skipped})")
                print("-" * 50)
                print()

        print("*" * 50)     
        print(f"[✅ DONE] Added: {added}, Skipped: {skipped}, Total: {total}")
        print("*" * 50)
        print()

        print("*" * 50)   
        print(f" ⇨ [INFO] Done in {time.time() - start_time:.2f}s")
        print("*" * 50)
        print()
        
    def search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k)

if __name__ == "__main__": 
    docs = get_data_loader()
    db = ChromaDB()
    db.add(docs)
    
    while True: 
        print("✷✷✷ Type your question...(press `q` to quit): ✷✷✷")

        question = input("")

        if question == "q":
            break

        results = db.search(question)

        print()
        print("=" * 50)
        print("🫴 Here are the results...")
        for doc in results:
            print(f"{doc.page_content}")
            print("." * 50)
        print("=" * 50)
        print()
