import json
from backend.llm import llm


SYSTEM_PROMPT = """
Você coleta informações para criar posts de redes sociais.

Informações úteis (todas opcionais):

- objetivo
- plataforma
- tema / produto
- público

Regras:

1. Tente descobrir algumas dessas informações conversando.
2. Nenhuma informação é obrigatória.
3. Se o usuário disser algo como "é isso", "pode gerar", "seria isso mesmo", etc, execute run_post_pipeline.
4. Se já houver contexto suficiente, também execute run_post_pipeline.
5. Nunca gere o post aqui. Apenas decida.

Responda SOMENTE em JSON neste formato:

{
 "action": "ask_user | run_post_pipeline",
 "message": "mensagem para o usuário",
 "state_updates": {
   "objetivo": null,
   "plataforma": null,
   "tema": null,
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
        "action": decision.get("action", "ask_user"),
        "message": decision.get("message", "Ok."),
        "state": state
}
