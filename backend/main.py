from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent_graph import graph
from backend.planner import planner
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

state = {
    "objetivo": None,
    "plataforma": None,
    "tema": None,
    "publico": None
}


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

    global state

    decision, state = planner(req.message, state)

    if decision["action"] == "ask_user":
        return {
            "reply": decision["message"]
        }

    if decision["action"] == "run_post_pipeline":

        result = graph.invoke(state)

        return {
            "post": result["post_final"]
        }
