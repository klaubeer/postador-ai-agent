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

    print("\n===== NEW REQUEST =====")
    print("SESSION:", req.session_id)
    print("MESSAGE RECEIVED:", req.message)

    state = get_session_state(req.session_id)
    msg = req.message.lower().strip()

    print("CURRENT STATE:", state)

    # -------------------------
    # geração de imagem
    # -------------------------

    if state.get("awaiting_image_approval"):

        print("AWAITING IMAGE APPROVAL MODE")
        print("USER MESSAGE:", msg)

        if "gerar" in msg:

            from backend.image_gen import generate_image

            prompt = state.get("image_prompt")

            print("GENERATING IMAGE WITH PROMPT:", prompt)

            if not prompt:
                print("ERROR: image_prompt vazio")
                return {
                    "message": "Erro: prompt de imagem não encontrado."
                }

            image_url = generate_image(prompt)

            print("IMAGE URL RETURNED:", image_url)

            state["image_url"] = image_url
            state["awaiting_image_approval"] = False

            sessions[req.session_id] = state

            print("UPDATED STATE:", state)

            return {
                "image": image_url
            }

        print("USER DID NOT CONFIRM IMAGE GENERATION")

        return {
            "message": "Digite **gerar** para criar a imagem."
        }

    # -------------------------
    # planner
    # -------------------------

    print("RUNNING PLANNER")

    decision = planner(req.message, state)

    print("PLANNER DECISION:", decision)

    state = decision["state"]

    required = ["objetivo", "plataforma", "tema"]

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

        # salva novo estado na sessão
        sessions[req.session_id] = result

        return {
            "post": result["post_final"],
            "state": result
        }

    print("ASKING USER MORE INFO")

    return {
        "message": decision["message"],
        "state": state
    }
