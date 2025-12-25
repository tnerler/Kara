from vector_database.chromadb_class import ChromaDB
from llm.model import get_llm
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
import json
from dotenv import load_dotenv

load_dotenv()

class Kara:
    def __init__(self, session_id: str = None):
        self.session_id = session_id
        self.db = ChromaDB()  # Load existing DB
        self.chain = self._build_chain()

        from utils.preprocess_data import get_data_loader
        docs = get_data_loader()
        if docs:
            self.db.add(docs)
            print(f"[INFO] Added {len(docs)} documents to DB.")
        else:
            print("[INFO] No local docs found. Using existing Chroma DB.")

    def _build_chain(self):
        with open("prompt_template/templates.json", "r", encoding="utf-8") as f:
            templates = json.load(f)

    
        system_message = templates[0]["system_message_prompt"]
        human_message = templates[0]["human_message_prompt"]

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_message),
                HumanMessagePromptTemplate.from_template(human_message),
            ]
        )

        model = get_llm(model_provider="openai")
        return prompt | model | StrOutputParser()

    def retrieve(self, question: str, k: int = 5):
        start = time.time()
        results = self.db.search(question, k=k)
        docs = [doc.page_content for doc in results[:k]]
        print(f"Retrieved {len(docs)} chunks in {round(time.time()-start,2)}s")
        return docs

    def generate(self, question: str, context_docs=None):
        start = time.time()
        if context_docs is None:
            context_docs = self.retrieve(question)

        docs_content = "\n\n".join(context_docs)
        input_data = {"question": question, "context": docs_content}
        answer = self.chain.invoke(input_data)
        print(f"The Generating Part took {round(time.time()-start,2)}s")
        return answer


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Kara - Tuana Erler's Personal Assistant")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 50)

    kara = Kara()

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Kara: Goodbye! 👋")
            break
        try:
            answer = kara.generate(question)
            print("\nKara:", answer)
        except Exception as e:
            print(f"[ERROR] {e}")
