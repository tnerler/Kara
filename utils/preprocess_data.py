import os 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from pathlib import Path
from utils._hash import compute_hash


def get_data_loader():

    root_path = Path("data")
    
    mds = root_path.glob("*.md")
    
    all_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

    for md_path in mds: 
        file_name = md_path.name

        try:
            loader = TextLoader(str(md_path), encoding="utf-8")
            docs = loader.load()
            split_docs = text_splitter.split_documents(docs)

            for doc in split_docs: 
                doc.metadata["hash"] = compute_hash(doc.page_content)
                doc.metadata["source_file"] = file_name


            all_docs.extend(split_docs)
        except Exception as e: 
            print(f"Error in {file_name}: {e}")
    
    print("*" * 50)
    print(f"🫸 --- TOTAL DOCUMENTS: {len(all_docs)} ---")
    print("*" * 50)
    print()
    return all_docs

if __name__ == "__main__": 
    get_data_loader()