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

# memória de sessões
sessions = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str


def get_session_state(session_id):

    if session_id not in sessions:
        sessions[session_id] = {
            "objetivo": None,
            "plataforma": None,
            "tema": None,
            "publico": None
        }

    return sessions[session_id]


@app.post("/post")
def create_post(req: ChatRequest):

    state = get_session_state(req.session_id)

    # planner decide próximo passo
    decision, state = planner(req.message, state)

    # salva estado atualizado
    sessions[req.session_id] = state

    if decision["action"] == "ask_user":
        return {
            "reply": decision["message"]
        }

    if decision["action"] == "run_post_pipeline":

        result = graph.invoke(state)

        # atualizar sessão com resultado final
        sessions[req.session_id] = result

        return {
            "post": result["post_final"]
        }

    # fallback de segurança
    return {
        "reply": "Não consegui entender. Pode reformular?"
    }
