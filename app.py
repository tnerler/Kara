import os 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from chatbot.rag import Kara
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

chatbot: Optional[Kara] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chatbot
    try:

        chatbot = Kara()
        print("[i] Chatbot initialized!")

    except Exception as e:
        print(f"[!] Error in startup: {e}")
        raise

    yield
    print("[!] Shutting down...")

app = FastAPI(
    title="Kara API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

class AskMessage(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="Question")
    session_id: Optional[str] = Field(None, description="Session identifier")

    @field_validator('question')
    def question_empty_checker(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty or whitespace only.')
        return v.strip()
    
class AskResponse(BaseModel):
    answer: str
    session_id: Optional[str] = Field(None, description="Session identifier")

def get_chatbot():
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chatbot is not available."
        )
    return chatbot


@app.post("/api/chat", response_model=AskResponse, status_code=status.HTTP_200_OK)
async def ask_question(msg: AskMessage):
    try:

        # Initialize session_id
        session_id = msg.session_id or "default_session"
        global chatbot
        if not chatbot:
            chatbot = Kara(session_id=session_id)
        
        state = {
            "question": msg.question,
            "context": [],
            "answer": "",
        }

        retrieval_result = chatbot.retrieve(msg.question)
        state["context"] = retrieval_result

        
        answer = chatbot.generate(msg.question, retrieval_result)
        state["answer"] = answer


        return AskResponse(
            answer=state["answer"],
            session_id=session_id
        )

    except Exception as e:
        print(f"[!] Error when user try to ask a question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your question: {str(e)}"
        )

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

