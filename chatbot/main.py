from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from summarization import SummarizationInferenceService
from chatbot_inference import ChatbotInference


class ChatbotRequest(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    answer: str
    length: int

class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    length: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models once at startup — not on every request
    global chatbot
    chatbot = ChatbotInference(artifacts=r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\chatbot\chatbot_artifacts")

    global summarizer
    summarizer = SummarizationInferenceService()
    print("Models loaded!")
    yield
    summarizer = None
    # Cleanup on shutdown (optional)
    #global chatbot
    #chatbot = None


def get_summarizer():
    return summarizer

def get_chatbot():
    return chatbot

app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}

# NOTE: For later, go to this Claude chat to build the chatbot inference service: https://claude.ai/chat/05916b5c-7cd5-450a-914e-7f0962ff739d

@app.post("/generate_answer", response_model=ChatbotResponse)
def generate_answer(data: ChatbotRequest, svc: ChatbotInference = Depends(get_chatbot)):
    print(data.question)
    answer = svc.generate_response(data.question)
    print(answer)
    return ChatbotResponse(answer=answer, length=len(answer))

@app.post("/generate_summary", response_model=SummaryResponse)
def generate_summary(data: SummaryRequest, svc: SummarizationInferenceService = Depends(get_summarizer)):
    summary = svc.summarize(data.text)
    return SummaryResponse(summary=summary, length=len(summary))