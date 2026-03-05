import json
from llm import llm


def extract_briefing(state):

    prompt = f"""
Extraia o briefing do pedido:

{state["user_input"]}

Retorne JSON:

objetivo
plataforma
publico
tema
"""

    result = llm(prompt)

    data = json.loads(result)

    state.update(data)

    return state
