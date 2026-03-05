from backend.llm import llm


def generate_ideas(state):

    prompt = f"""
Crie 3 ideias de post curtas.

Objetivo: {state.get("objetivo")}
Plataforma: {state.get("plataforma")}
Tema: {state.get("tema")}
Público: {state.get("publico")}

Regras:
- cada ideia no máximo 8 palavras
- sem explicação
- apenas lista numerada
"""

    ideias = llm(prompt)

    state["ideias"] = ideias

    return state


def select_best_idea(state):

    prompt = f"""
Escolha a melhor ideia para viralizar.

Ideias:
{state.get("ideias")}

Regras:
- retorne apenas o número da ideia
- sem explicação
"""

    melhor = llm(prompt)

    state["melhor_ideia"] = melhor

    return state


def generate_caption(state):

    prompt = f"""
Crie legenda curta.

Ideia:
{state.get("melhor_ideia")}

Plataforma:
{state.get("plataforma")}

Regras:
- máximo 1 frase
- incluir CTA
"""

    legenda = llm(prompt)

    state["legenda"] = legenda

    return state


def generate_image_prompt(state):

    prompt = f"""
Crie prompt de imagem curto.

Ideia:
{state.get("melhor_ideia")}

Regras:
- máximo 15 palavras
- estilo visual claro
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
Crie hashtags para este post.

Ideia:
{state.get("melhor_ideia")}

Plataforma:
{plataforma}

Regras:
- máximo 5 hashtags
- retorne apenas hashtags
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
