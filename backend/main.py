from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

    resposta = f"""
Aqui está um exemplo de post:

📢 {req.message}

✨ Descubra como isso pode transformar seu dia.

#marketing #socialmedia #conteudo
"""

    return {"reply": resposta}
