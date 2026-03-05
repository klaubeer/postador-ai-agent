from backend.llm import llm


def generate_ideas(state):

    prompt = f"""
Crie 5 ideias de post para redes sociais.

Objetivo: {state.get("objetivo")}
Plataforma: {state.get("plataforma")}
Tema: {state.get("tema")}
Público: {state.get("publico")}

Retorne as ideias de forma clara e numerada.
"""

    ideias = llm(prompt)

    state["ideias"] = ideias

    return state


def select_best_idea(state):

    prompt = f"""
Escolha a melhor ideia para viralizar.

Ideias:

{state.get("ideias")}

Explique brevemente e retorne apenas a ideia escolhida.
"""

    melhor = llm(prompt)

    state["melhor_ideia"] = melhor

    return state


def generate_caption(state):

    prompt = f"""
Crie uma legenda envolvente para redes sociais.

Ideia:
{state.get("melhor_ideia")}

Plataforma:
{state.get("plataforma")}

Inclua um CTA forte.
"""

    legenda = llm(prompt)

    state["legenda"] = legenda

    return state


def generate_image_prompt(state):

    prompt = f"""
Crie um prompt detalhado para gerar uma imagem com IA.

Baseado nesta ideia de post:

{state.get("melhor_ideia")}

Descreva a cena visual claramente.
"""

    image_prompt = llm(prompt)

    state["image_prompt"] = image_prompt

    return state


def generate_hashtags(state):

    plataforma = state.get("plataforma")

    if plataforma and plataforma.lower() not in ["instagram", "tiktok"]:
        state["hashtags"] = ""
        return state

    prompt = f"""
Crie hashtags relevantes para este post.

Ideia:
{state.get("melhor_ideia")}

Plataforma:
{plataforma}

Retorne apenas hashtags.
"""

    hashtags = llm(prompt)

    state["hashtags"] = hashtags

    return state


def format_post(state):

    state["post_final"] = f"""
🎯 Ideia
{state.get("melhor_ideia")}

✍️ Legenda
{state.get("legenda")}

🖼️ Prompt de imagem
{state.get("image_prompt")}

🏷️ Hashtags
{state.get("hashtags")}
"""

    return state
