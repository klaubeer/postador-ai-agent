from backend.llm import llm


def generate_idea(state):

    prompt = f"""
Crie uma ideia de post para redes sociais.

Produto/Tema: {state.get("tema")}
Plataforma: {state.get("plataforma")}
Público: {state.get("publico")}
Objetivo: {state.get("objetivo")}

Regras:
- máximo 50 palavras
- explicar claramente o conceito do post
- usar o produto ou tema
- pensar no público
- sem hashtags
- sem emojis
"""

    ideia = llm(prompt)

    if ideia:
        ideia = ideia.strip()

    # mantém mesmo nome para não quebrar pipeline
    state["melhor_ideia"] = ideia or ""

    return state


def generate_caption(state):

    prompt = f"""
Crie legenda curta para redes sociais.

Ideia: {state.get("melhor_ideia")}
Produto/Tema: {state.get("tema")}
Público: {state.get("publico")}
Plataforma: {state.get("plataforma")}

Regras:
- mencionar o produto
- falar com o público
- máximo 1 frase
- incluir CTA
"""

    legenda = llm(prompt)

    if legenda:
        legenda = legenda.strip()

    state["legenda"] = legenda or ""

    return state


def generate_hashtags(state):

    plataforma = state.get("plataforma")

    # hashtags fazem sentido só para algumas redes
    if plataforma and plataforma.lower() not in ["instagram", "tiktok"]:
        state["hashtags"] = ""
        return state

    prompt = f"""
Crie até 5 hashtags para redes sociais.

Produto/Tema: {state.get("tema")}
Público: {state.get("publico")}

Retorne apenas hashtags separadas por espaço.
"""

    hashtags = llm(prompt)

    if hashtags:

        hashtags = hashtags.replace("\n", " ").replace(",", " ").strip()

        tags = hashtags.split()

        # garante #
        tags = [t if t.startswith("#") else f"#{t}" for t in tags]

        # máximo 5
        tags = tags[:5]

        hashtags = " ".join(tags)

    state["hashtags"] = hashtags or ""

    return state


def generate_image_prompt(state):

    prompt = f"""
Write a short prompt for an AI image generator.

Product/Theme: {state.get("tema")}
Idea: {state.get("melhor_ideia")}
Audience: {state.get("publico")}

Rules:
- max 15 words
- clearly show the product
- specify visual style
"""

    image_prompt = llm(prompt)

    if image_prompt:
        image_prompt = image_prompt.strip()

    state["image_prompt"] = image_prompt or ""

    return state


def format_post(state):

    ideia = state.get("melhor_ideia", "")
    legenda = state.get("legenda", "")
    hashtags = state.get("hashtags", "")
    image_prompt = state.get("image_prompt", "")

    hashtags_section = f"\n🏷️ Hashtags\n{hashtags}" if hashtags else ""

    state["post_final"] = f"""🎯 Ideia
{ideia}

✍️ Legenda
{legenda}
{hashtags_section}

🖼️ Prompt de imagem (opcional)
{image_prompt}
"""

    return state
