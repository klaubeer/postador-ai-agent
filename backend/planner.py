import json
from backend.llm import llm


def planner(user_input, state):

    prompt = f"""
Estado atual:
{state}

Mensagem do usuário:
{user_input}
"""

    result = llm(prompt)

    try:
        decision = json.loads(result)
    except:
        decision = {
            "action": "ask_user",
            "message": "Pode me contar um pouco mais sobre o post que você quer criar?",
            "state_updates": {}
        }

    # atualizar estado
    for k, v in decision.get("state_updates", {}).items():
        if v:
            state[k] = v

    return decision, state
