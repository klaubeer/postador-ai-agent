from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent_chat   # ← novo import

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    sessionId: str


@app.post("/chat")
async def chat(req: ChatRequest):

    resposta = agent_chat(req.sessionId, req.message)  # ← chama o agente

    return {"reply": resposta}
