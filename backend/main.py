from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent_graph import graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.post("/post")
def create_post(req: ChatRequest):

    state = {
        "user_input": req.message
    }

    result = graph.invoke(state)

    return {
        "post": result["post_final"]
    }
