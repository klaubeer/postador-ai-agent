from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_graph import agent_graph_chat


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

    resposta = agent_graph_chat(req.sessionId, req.message)
    
    return {"reply": resposta}


@app.get("/")
def root():
    return {"status": "Postador API online"}
