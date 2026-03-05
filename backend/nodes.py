import json
from backend.llm import llm


def extract_briefing(state):

    prompt = f"""
Extraia o briefing do pedido abaixo.

Pedido:
{state["user_input"]}

Retorne APENAS JSON válido neste formato:

{{
 "objetivo": "...",
 "plataforma": "...",
 "publico": "...",
 "tema": "..."
}}

Se algum campo não existir use null.
"""

    result = llm(prompt)

    try:
        data = json.loads(result)
    except:
        data = {}

    state["objetivo"] = data.get("objetivo")
    state["plataforma"] = data.get("plataforma")
    state["publico"] = data.get("publico")
    state["tema"] = data.get("tema")

    return state


def generate_ideas(state):

    prompt = f"""
Crie 5 ideias de post para redes sociais.

Objetivo: {state.get("objetivo")}
Plataforma: {state.get("plataforma")}
Tema: {state.get("tema")}
Público: {state.get("publico")}
"""

    ideias = llm(prompt)

    state["ideias"] = ideias

    return state


def select_best_idea(state):

    prompt = f"""
Escolha a melhor ideia para viralizar.

Ideias:

{state["ideias"]}

Explique brevemente e retorne apenas a ideia escolhida.
"""

    state["melhor_ideia"] = llm(prompt)

    return state


def generate_caption(state):

    prompt = f"""
Crie uma legenda para redes sociais.

Ideia:
{state["melhor_ideia"]}

Plataforma:
{state.get("plataforma")}
"""

    state["legenda"] = llm(prompt)

    return state


def generate_image_prompt(state):

    prompt = f"""
Crie um prompt para gerar imagem com IA.

Baseado na ideia:

{state["melhor_ideia"]}
"""

    state["image_prompt"] = llm(prompt)

    return state


def generate_hashtags(state):

    prompt = f"""
Crie hashtags relevantes para:

{state["melhor_ideia"]}

Plataforma:
{state.get("plataforma")}
"""

    state["hashtags"] = llm(prompt)

    return state


def format_post(state):

    state["post_final"] = f"""
🎯 Ideia
{state["melhor_ideia"]}

✍️ Legenda
{state["legenda"]}

🖼️ Prompt de imagem
{state["image_prompt"]}

🏷️ Hashtags
{state["hashtags"]}
"""

    return state
