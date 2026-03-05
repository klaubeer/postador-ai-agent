from fastapi import FastAPI
from pydantic import BaseModel

from agent_graph import graph

app = FastAPI()


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
