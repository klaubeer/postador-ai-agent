from backend.llm import llm


def generate_content(state):
    """Gera legenda + hashtags num único prompt robusto."""

    tema = state.get("tema", "")
    plataforma = state.get("plataforma", "Instagram")
    objetivo = state.get("objetivo", "engajar")
    publico = state.get("publico", "público geral")
    detalhes = state.get("detalhes", "")

    prompt = f"""Você é um social media expert. Crie o conteúdo de um post para redes sociais.

CONTEXTO:
- Tema/Produto: {tema}
- Plataforma: {plataforma}
- Objetivo: {objetivo}
- Público-alvo: {publico}
- Detalhes extras: {detalhes or 'nenhum'}

ENTREGUE EXATAMENTE NESTE FORMATO (sem markdown, sem explicações):

LEGENDA:
[Escreva uma legenda criativa, envolvente, com CTA. Máximo 3 frases. Adequada para {plataforma}.]

HASHTAGS:
[5 hashtags relevantes e populares, separadas por espaço. Ex: #exemplo1 #exemplo2]"""

    result = llm(prompt)

    # parse do resultado
    legenda = ""
    hashtags = ""

    if "LEGENDA:" in result and "HASHTAGS:" in result:
        parts = result.split("HASHTAGS:")
        legenda = parts[0].replace("LEGENDA:", "").strip()
        hashtags = parts[1].strip()
    else:
        legenda = result.strip()

    # garante formato das hashtags
    if hashtags:
        tags = hashtags.replace("\n", " ").replace(",", " ").split()
        tags = [t if t.startswith("#") else f"#{t}" for t in tags if t]
        hashtags = " ".join(tags[:5])

    state["legenda"] = legenda
    state["hashtags"] = hashtags

    return state


def generate_image_prompt(state):
    """Gera um prompt detalhado para geração de imagem."""

    tema = state.get("tema", "")
    legenda = state.get("legenda", "")
    plataforma = state.get("plataforma", "Instagram")
    publico = state.get("publico", "")
    detalhes = state.get("detalhes", "")

    prompt = f"""You are an expert at writing prompts for AI image generators (Stable Diffusion / FLUX).

Create a detailed image prompt for a social media post.

CONTEXT:
- Product/Theme: {tema}
- Caption: {legenda}
- Platform: {plataforma}
- Audience: {publico or 'general'}
- Extra details: {detalhes or 'none'}

RULES:
- Write in English
- Be specific about: subject, composition, lighting, color palette, style
- Make it visually striking and scroll-stopping
- Appropriate for {plataforma}
- Maximum 60 words
- Do NOT include text/words in the image
- Return ONLY the prompt, nothing else"""

    image_prompt = llm(prompt)

    if image_prompt:
        image_prompt = image_prompt.strip().strip('"').strip("'")

    state["image_prompt"] = image_prompt or ""

    return state
