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
            "publico": None,
            "image_prompt": None,
            "image_url": None,
            "awaiting_image_approval": False
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
    msg = req.message.lower().strip()

    # -------------------------
    # geração de imagem
    # -------------------------

    if state.get("awaiting_image_approval"):

        if "gerar imagem" in msg:

            from backend.image_gen import generate_image

            prompt = state.get("image_prompt")

            if not prompt:
                return {
                    "message": "Erro: prompt de imagem não encontrado."
                }

            image_url = generate_image(prompt)

            state["image_url"] = image_url
            state["awaiting_image_approval"] = False

            sessions[req.session_id] = state

            return {
                "image": image_url
            }

        return {
            "message": "Digite **gerar imagem** para criar a imagem."
        }

    # -------------------------
    # planner
    # -------------------------

    decision = planner(req.message, state)
    state = decision["state"]

    required = ["objetivo", "plataforma", "tema"]

    if decision["action"] == "run_post_pipeline":

        if not all(state.get(k) for k in required):

            return {
                "message": "Preciso de mais algumas informações antes de gerar o post."
            }

        result = graph.invoke(state)

        # salva novo estado na sessão
        sessions[req.session_id] = result

        return {
            "post": result["post_final"],
            "state": result
        }

    return {
        "message": decision["message"],
        "state": state
    }
