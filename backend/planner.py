import json
from backend.llm import llm


SYSTEM_PROMPT = """
Você é um assistente que ajuda a criar posts para redes sociais.

Seu trabalho:

1. Descobrir o objetivo do post
(vender, engajar, educar, inspirar, entreter)

2. Descobrir a plataforma
Instagram, Facebook, TikTok, LinkedIn, X ou YouTube Shorts

3. Descobrir o tema / produto / empresa / público

4. Quando tiver informação suficiente gere 3 ideias contendo:

🎯 Título
✍️ Legenda com CTA
🖼️ Sugestão de imagem
🏷️ Hashtags (se Instagram ou TikTok)

5. Peça para o usuário escolher uma ideia.

Se faltar informação, pergunte naturalmente.

Responda APENAS em JSON neste formato:

{
 "action": "ask_user | run_post_pipeline",
 "message": "mensagem para o usuário",
 "state_updates": {
   "objetivo": "...",
   "plataforma": "...",
   "tema": "...",
   "publico": "..."
 }
}
"""


def extract_json(text: str):
    """
    Tenta extrair JSON mesmo que o LLM coloque texto extra.
    """
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])


def planner(user_input: str, state: dict):

    prompt = f"""
Estado atual da conversa:

objetivo: {state.get("objetivo")}
plataforma: {state.get("plataforma")}
tema: {state.get("tema")}
publico: {state.get("publico")}

Mensagem do usuário:
{user_input}
"""

    result = llm(SYSTEM_PROMPT + "\n\n" + prompt)

    decision = extract_json(result)

    # --------- CORREÇÃO CRÍTICA ---------
    updates = decision.get("state_updates", {})

    for key, value in updates.items():
        if value:
            state[key] = value
    # ------------------------------------

    return {
        "action": decision["action"],
        "message": decision["message"],
        "state": state
    }
