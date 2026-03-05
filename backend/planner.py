import json
from backend.llm import llm


SYSTEM_PROMPT = """
Você coleta informações para criar posts de redes sociais.

Descubra:
- objetivo (vender, engajar, educar, inspirar, entreter)
- plataforma (Instagram, Facebook, TikTok, LinkedIn, X, YouTube Shorts)
- tema / produto / empresa
- público-alvo

Regras:

1. Se faltar alguma informação → pergunte ao usuário.
2. Se já tiver informações suficientes → responda com action="run_post_pipeline".
3. Nunca gere o post aqui.

Responda SOMENTE em JSON neste formato:

{
 "action": "ask_user",
 "message": "Qual é o público-alvo do post?",
 "state_updates": {
   "objetivo": "vender",
   "plataforma": "LinkedIn",
   "tema": "agentes de IA",
   "publico": null
 }
}
"""


def extract_json(text: str):

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception:
        print("LLM retornou JSON inválido:")
        print(text)

        return {
            "action": "ask_user",
            "message": "Desculpe, houve um erro. Pode repetir?",
            "state_updates": {}
        }

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

    result = llm(f"{SYSTEM_PROMPT}\n\n{prompt}")

    decision = extract_json(result)

    # Atualiza estado da conversa
    updates = decision.get("state_updates", {})

    for key, value in updates.items():
        if value:
            state[key] = value

    return {
        "action": decision["action"],
        "message": decision["message"],
        "state": state
    }
