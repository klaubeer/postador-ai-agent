from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agent_graph import graph
from backend.planner import planner
from backend.image_gen import generate_image
from backend.llm import reset_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# sessão em memória
# -------------------------

sessions: dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    if session_id not in sessions:
        sessions[session_id] = {
            "state": {
                "objetivo": None,
                "plataforma": None,
                "tema": None,
                "publico": None,
                "detalhes": None,
                "post_gerado": False,
            },
            "messages": [],
        }
    return sessions[session_id]


# -------------------------
# schemas
# -------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ImageRequest(BaseModel):
    session_id: str


# -------------------------
# CHAT
# -------------------------

@app.post("/api/chat")
def chat(req: ChatRequest):

    session = get_session(req.session_id)
    state = session["state"]
    messages = session["messages"]

    # se já gerou post, qualquer mensagem nova reseta pra novo post
    if state.get("post_gerado"):
        bot_msg = "Que bom que curtiu! Quer criar outro post? Me conta o tema."
        messages.append({"role": "user", "content": req.message})
        messages.append({"role": "assistant", "content": bot_msg})

        # reseta estado pra novo post mas mantém histórico
        session["state"] = {
            "objetivo": None,
            "plataforma": None,
            "tema": None,
            "publico": None,
            "detalhes": None,
            "post_gerado": False,
        }

        return {"message": bot_msg}

    # adiciona mensagem ao histórico
    messages.append({"role": "user", "content": req.message})

    # planner decide o fluxo
    decision = planner(messages, state, session_id=req.session_id)

    state = decision["state"]
    session["state"] = state

    # --- gerar post ---
    if decision["action"] == "run_post_pipeline":

        if not state.get("tema"):
            bot_msg = "Qual é o tema ou produto do post?"
            messages.append({"role": "assistant", "content": bot_msg})
            return {"message": bot_msg}

        # roda pipeline
        result = graph.invoke(state)

        # atualiza estado
        state.update({
            "ideias": result.get("ideias", ""),
            "melhor_ideia": result.get("melhor_ideia", ""),
            "legenda": result.get("legenda", ""),
            "hashtags": result.get("hashtags", ""),
            "image_prompt": result.get("image_prompt", ""),
            "post_gerado": True,
        })
        session["state"] = state

        # gera imagem
        image_url = ""
        image_prompt = result.get("image_prompt", "")
        if image_prompt:
            image_result = generate_image(image_prompt)
            image_url = image_result.get("image_url", "")
            if image_url:
                state["image_url"] = image_url

        # monta post final completo
        post = ""

        if result.get("ideias"):
            post += f"💡 Ideias de post\n{result['ideias']}\n\n"

        if result.get("melhor_ideia"):
            post += f"🎯 Melhor ideia (detalhada)\n{result['melhor_ideia']}\n\n"

        if result.get("legenda"):
            post += f"✍️ Legenda\n{result['legenda']}"

        if result.get("hashtags"):
            post += f"\n\n🏷️ Hashtags\n{result['hashtags']}"

        post = post.strip()
        state["post_final"] = post
        session["state"] = state

        messages.append({"role": "assistant", "content": post})

        return {
            "post": post,
            "image_url": image_url,
        }

    # --- continuar conversa ---
    bot_msg = decision["message"]
    messages.append({"role": "assistant", "content": bot_msg})

    return {"message": bot_msg}


# -------------------------
# GERAR NOVA IMAGEM (fallback manual)
# -------------------------

@app.post("/api/gerar-imagem")
def gerar_imagem(req: ImageRequest):

    session = get_session(req.session_id)
    state = session["state"]

    prompt = state.get("image_prompt")

    if not prompt:
        return {"error": "Nenhum prompt de imagem disponível."}

    result = generate_image(prompt)

    if "error" in result:
        return result

    state["image_url"] = result["image_url"]
    return {"image_url": result["image_url"]}


# -------------------------
# RESET
# -------------------------

@app.post("/api/reset")
def reset(req: ImageRequest):
    session_id = req.session_id
    sessions.pop(session_id, None)
    reset_session(session_id)
    return {"ok": True}
