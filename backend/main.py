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
            "image_url": None
        }
    return sessions[session_id]


# -------------------------
# request schema
# -------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ImageRequest(BaseModel):
    session_id: str


# -------------------------
# CHAT ENDPOINT
# -------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    print("\n===== NEW REQUEST =====")
    print("SESSION:", req.session_id)
    print("MESSAGE RECEIVED:", req.message)

    state = get_session_state(req.session_id)

    print("CURRENT STATE:", state)

    # planner decide fluxo
    decision = planner(req.message, state)

    print("PLANNER DECISION:", decision)

    state = decision["state"]

    required = ["objetivo", "plataforma", "tema"]

    # -------------------------
    # gerar post
    # -------------------------

    if decision["action"] == "run_post_pipeline":

        print("ACTION: RUN POST PIPELINE")

        if not all(state.get(k) for k in required):

            print("MISSING REQUIRED INFO")

            return {
                "message": "Preciso de mais algumas informações antes de gerar o post."
            }

        print("RUNNING GRAPH PIPELINE")

        result = graph.invoke(state)

        print("GRAPH RESULT:", result)

        sessions[req.session_id] = result

        return {
            "post": result["post_final"],
            "state": result
        }

    # -------------------------
    # continuar conversa
    # -------------------------

    print("ASKING USER MORE INFO")

    sessions[req.session_id] = state

    return {
        "message": decision["message"],
        "state": state
    }


# -------------------------
# IMAGE GENERATION
# -------------------------

@app.post("/gerar-imagem")
def gerar_imagem(req: ImageRequest):

    print("\n===== IMAGE GENERATION =====")
    print("SESSION:", req.session_id)

    state = get_session_state(req.session_id)

    prompt = state.get("image_prompt")

    print("IMAGE PROMPT:", prompt)

    if not prompt:
        return {
            "error": "Prompt de imagem não encontrado."
        }

    from backend.image_gen import generate_image

    result = generate_image(prompt)

    # erro vindo da geração
    if "error" in result:

        print("IMAGE GENERATION FAILED:", result["error"])

        return result

    image = result["image"]

    print("IMAGE GENERATED")

    state["image_url"] = image
    sessions[req.session_id] = state

    return {
        "image": image
    }
