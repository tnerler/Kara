from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 

load_dotenv()

def get_llm(model_provider="openai"): 

    try: 
        if model_provider == "openai": 
            print("*"*50)
            print("[INFO] OpenAI is being used as LLM.")
            print("*"*50)
            print()


            return init_chat_model(model="gpt-4o-mini",
                                   model_provider=model_provider,
                                   api_key=os.getenv("OPENAI_API_KEY"),
                                   temperature=0.8)
        else:
            raise ValueError("Not providing this kind of model...Try again!")
    except Exception as e:
        print(f"Error in starting LLM: {e}")