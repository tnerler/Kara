from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv
load_dotenv()

def openai_embedding_model(): 

    """Returns the embedding model of OpenAI."""

    model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return model