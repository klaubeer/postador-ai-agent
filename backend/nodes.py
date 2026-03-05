import json
from backend.llm import llm


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

def generate_ideas(state):

    prompt = f"""
Crie 5 ideias de post.

Objetivo: {state["objetivo"]}
Plataforma: {state["plataforma"]}
Tema: {state["tema"]}
Público: {state["publico"]}
"""

    ideias = llm(prompt)

    state["ideias"] = ideias

    return state

def select_best_idea(state):

    prompt = f"""
Escolha a melhor ideia para viralizar.

Ideias:

{state["ideias"]}
"""

    state["melhor_ideia"] = llm(prompt)

    return state


def generate_caption(state):

    prompt = f"""
Crie uma legenda para redes sociais.

Ideia:
{state["melhor_ideia"]}

Plataforma:
{state["plataforma"]}
"""

    state["legenda"] = llm(prompt)

    return state


def generate_image_prompt(state):

    prompt = f"""
Crie um prompt de imagem IA.

Baseado na ideia:

{state["melhor_ideia"]}
"""

    state["image_prompt"] = llm(prompt)

    return state


def generate_hashtags(state):

    prompt = f"""
Crie hashtags para:

{state["melhor_ideia"]}

Plataforma:
{state["plataforma"]}
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
