from backend.llm import llm


# -------------------------
# IDEIA
# -------------------------

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
"""

    ideia = llm(prompt)

    if ideia:
        ideia = ideia.strip()

    state["melhor_ideia"] = ideia or ""

    return state


# -------------------------
# LEGENDA
# -------------------------

def generate_caption(state):

    prompt = f"""
Crie uma legenda curta para redes sociais.

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


# -------------------------
# HASHTAGS
# -------------------------

def generate_hashtags(state):

    plataforma = (state.get("plataforma") or "").lower()

    # normaliza plataformas
    if "insta" in plataforma:
        plataforma = "instagram"

    if "tik" in plataforma:
        plataforma = "tiktok"

    # só gerar hashtags nessas redes
    if plataforma not in ["instagram", "tiktok"]:
        state["hashtags"] = ""
        return state

    prompt = f"""
Crie até 5 hashtags para redes sociais.

Produto/Tema: {state.get("tema")}
Público: {state.get("publico")}

Regras:
- máximo 5
- populares
- relacionadas ao tema

Retorne apenas hashtags separadas por espaço.
"""

    hashtags = llm(prompt)

    if hashtags:

        hashtags = hashtags.replace("\n", " ").replace(",", " ").strip()

        tags = hashtags.split()

        # garante #
        tags = [t if t.startswith("#") else f"#{t}" for t in tags]

        tags = tags[:5]

        hashtags = " ".join(tags)

    state["hashtags"] = hashtags or ""

    return state


# -------------------------
# IMAGE PROMPT
# -------------------------

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


# -------------------------
# FORMAT POST
# -------------------------

def format_post(state):

    ideia = state.get("melhor_ideia", "")
    legenda = state.get("legenda", "")
    hashtags = state.get("hashtags", "")
    image_prompt = state.get("image_prompt", "")

    post = f"""🎯 Ideia
{ideia}

✍️ Legenda
{legenda}
"""

    if hashtags:
        post += f"""

🏷️ Hashtags
{hashtags}
"""

    if image_prompt:
        post += f"""

🖼️ Prompt de imagem
{image_prompt}
"""

    state["post_final"] = post

    return state
