from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.agent_graph import graph
from backend.planner import planner


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# sessão simples em memória
# -------------------------

sessions = {}


def get_session_state(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "objetivo": None,
            "plataforma": None,
            "tema": None,
            "publico": None
        }
    return sessions[session_id]


# -------------------------
# request schema
# -------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str


# -------------------------
# endpoint
# -------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    state = get_session_state(req.session_id)

    decision = planner(req.message, state)
    state = decision["state"]

    # -------- validação antes do pipeline --------

    required = ["objetivo", "plataforma", "tema"]

    if decision["action"] == "run_post_pipeline":
        if not all(state.get(k) for k in required):
            return {
                "message": "Preciso de mais algumas informações antes de gerar o post."
            }

        result = graph.invoke(state)

        return {
            "post": result["post_final"],
            "state": state
        }

    # --------------------------------------------

    return {
        "message": decision["message"],
        "state": state
    }
