from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agent_graph import ideas_graph, post_graph
from backend.planner import planner
from backend.image_gen import generate_image
from backend.llm import reset_session
from backend.nodes import VISUAL_STYLES

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


def new_state():
    return {
        "objetivo": None,
        "plataforma": None,
        "tema": None,
        "publico": None,
        "detalhes": None,
        "stage": "collecting",
    }


def get_session(session_id: str) -> dict:
    if session_id not in sessions:
        sessions[session_id] = {
            "state": new_state(),
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
    stage = state.get("stage", "collecting")

    messages.append({"role": "user", "content": req.message})

    # ===========================
    # STAGE: collecting — planner coleta contexto
    # ===========================
    if stage == "collecting":
        decision = planner(messages, state, session_id=req.session_id)
        state = decision["state"]
        session["state"] = state

        if decision["action"] == "run_post_pipeline":
            if not state.get("tema"):
                bot_msg = "Qual é o tema ou produto do post?"
                messages.append({"role": "assistant", "content": bot_msg})
                return {"message": bot_msg}

            # gera 3 ideias
            result = ideas_graph.invoke(state)
            state["ideias_raw"] = result.get("ideias_raw", "")
            state["stage"] = "choosing_idea"
            session["state"] = state

            bot_msg = f"{result.get('ideias_raw', '')}\n\n---\nQual ideia você prefere? Responda com o número (1, 2 ou 3). Ou peça ajustes!"
            messages.append({"role": "assistant", "content": bot_msg})

            return {"message": bot_msg}

        # continuar conversa
        bot_msg = decision["message"]
        messages.append({"role": "assistant", "content": bot_msg})
        return {"message": bot_msg}

    # ===========================
    # STAGE: choosing_idea — usuário escolhe ideia
    # ===========================
    if stage == "choosing_idea":
        user_msg = req.message.strip()

        # extrai a ideia escolhida do texto completo
        ideias_raw = state.get("ideias_raw", "")
        ideia_escolhida = ""

        # tenta encontrar pela número
        for num in ["1", "2", "3"]:
            if num in user_msg:
                # extrai bloco da ideia
                marker = f"IDEIA {num}:"
                if marker in ideias_raw:
                    start = ideias_raw.index(marker)
                    # encontra o fim (próxima IDEIA ou fim do texto)
                    end = len(ideias_raw)
                    for next_num in ["1", "2", "3"]:
                        next_marker = f"IDEIA {next_num}:"
                        if next_marker in ideias_raw and ideias_raw.index(next_marker) > start + 1:
                            possible_end = ideias_raw.index(next_marker)
                            if possible_end < end and possible_end > start + len(marker):
                                end = possible_end
                    ideia_escolhida = ideias_raw[start:end].strip()
                break

        if not ideia_escolhida:
            # se não achou número, assume que o usuário descreveu preferência
            ideia_escolhida = f"Preferência do usuário: {user_msg}\n\nBaseado em:\n{ideias_raw}"

        state["ideia_escolhida"] = ideia_escolhida
        state["stage"] = "choosing_style"
        session["state"] = state

        styles_text = "\n".join(f"  {k}. {v}" for k, v in VISUAL_STYLES.items())
        bot_msg = f"Boa escolha! Agora, qual estilo visual você prefere para a imagem?\n\n{styles_text}\n\nResponda com o número (1, 2, 3 ou 4)."
        messages.append({"role": "assistant", "content": bot_msg})

        return {"message": bot_msg}

    # ===========================
    # STAGE: choosing_style — usuário escolhe estilo visual
    # ===========================
    if stage == "choosing_style":
        user_msg = req.message.strip()

        # extrai número do estilo
        estilo = "1"  # default
        for num in ["1", "2", "3", "4"]:
            if num in user_msg:
                estilo = num
                break

        state["estilo_visual"] = estilo
        session["state"] = state

        style_name = VISUAL_STYLES.get(estilo, VISUAL_STYLES["1"])

        # gera post final + image prompt
        result = post_graph.invoke(state)

        state.update({
            "legenda": result.get("legenda", ""),
            "hashtags": result.get("hashtags", ""),
            "descricao_imagem": result.get("descricao_imagem", ""),
            "image_prompt": result.get("image_prompt", ""),
            "stage": "done",
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

        # monta post final
        post = ""

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
            "style": style_name,
        }

    # ===========================
    # STAGE: done — post já gerado
    # ===========================
    if stage == "done":
        # reseta pra novo post
        session["state"] = new_state()

        bot_msg = "Que bom que curtiu! Quer criar outro post? Me conta o tema."
        messages.append({"role": "assistant", "content": bot_msg})
        return {"message": bot_msg}

    # fallback
    return {"message": "Como posso ajudar?"}


# -------------------------
# GERAR NOVA IMAGEM
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
