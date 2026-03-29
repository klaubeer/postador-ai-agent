from backend.llm import llm


def generate_content(state):
    """Gera ideias criativas + legenda + hashtags num único prompt robusto."""

    tema = state.get("tema", "")
    plataforma = state.get("plataforma", "Instagram")
    objetivo = state.get("objetivo", "engajar")
    publico = state.get("publico", "público geral")
    detalhes = state.get("detalhes", "")

    prompt = f"""Você é um social media expert criativo. Crie o conteúdo completo de um post para redes sociais.

CONTEXTO:
- Tema/Produto: {tema}
- Plataforma: {plataforma}
- Objetivo: {objetivo}
- Público-alvo: {publico}
- Detalhes extras: {detalhes or 'nenhum'}

ENTREGUE EXATAMENTE NESTE FORMATO (sem markdown extra, sem explicações fora do formato):

IDEIAS:
1. [Primeira ideia criativa de post — descreva o conceito, abordagem e formato sugerido em 2-3 frases]
2. [Segunda ideia criativa — uma abordagem diferente da primeira]
3. [Terceira ideia criativa — uma abordagem diferente das anteriores]

MELHOR IDEIA:
[Escolha a melhor das 3 ideias acima e explique em detalhes como executar o post: o que mostrar, que texto colocar na imagem/vídeo, qual o gancho pra prender atenção. Seja específico e prático. 3-5 frases.]

LEGENDA:
[Escreva uma legenda envolvente e criativa. Máximo 3 frases. Inclua CTA (call-to-action). Use o tom adequado para {plataforma} e {publico}.]

HASHTAGS:
[5 hashtags relevantes e populares, separadas por espaço. Ex: #exemplo1 #exemplo2]"""

    result = llm(prompt)

    # parse do resultado
    ideias = ""
    melhor_ideia = ""
    legenda = ""
    hashtags = ""

    sections = {}
    current_section = None
    current_lines = []

    for line in result.split("\n"):
        line_stripped = line.strip()

        if line_stripped.startswith("IDEIAS:"):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = "ideias"
            current_lines = []
            rest = line_stripped.replace("IDEIAS:", "").strip()
            if rest:
                current_lines.append(rest)
        elif line_stripped.startswith("MELHOR IDEIA:"):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = "melhor_ideia"
            current_lines = []
            rest = line_stripped.replace("MELHOR IDEIA:", "").strip()
            if rest:
                current_lines.append(rest)
        elif line_stripped.startswith("LEGENDA:"):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = "legenda"
            current_lines = []
            rest = line_stripped.replace("LEGENDA:", "").strip()
            if rest:
                current_lines.append(rest)
        elif line_stripped.startswith("HASHTAGS:"):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = "hashtags"
            current_lines = []
            rest = line_stripped.replace("HASHTAGS:", "").strip()
            if rest:
                current_lines.append(rest)
        else:
            if current_section:
                current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    ideias = sections.get("ideias", "")
    melhor_ideia = sections.get("melhor_ideia", "")
    legenda = sections.get("legenda", "")
    hashtags = sections.get("hashtags", "")

    # garante formato das hashtags
    if hashtags:
        tags = hashtags.replace("\n", " ").replace(",", " ").split()
        tags = [t if t.startswith("#") else f"#{t}" for t in tags if t]
        hashtags = " ".join(tags[:5])

    state["ideias"] = ideias
    state["melhor_ideia"] = melhor_ideia
    state["legenda"] = legenda
    state["hashtags"] = hashtags

    return state


def generate_image_prompt(state):
    """Gera um prompt detalhado para geração de imagem."""

    tema = state.get("tema", "")
    melhor_ideia = state.get("melhor_ideia", "")
    plataforma = state.get("plataforma", "Instagram")
    publico = state.get("publico", "")
    detalhes = state.get("detalhes", "")

    prompt = f"""You are an expert at writing prompts for AI image generators (Stable Diffusion / FLUX).

Create a detailed image prompt for a social media post.

CONTEXT:
- Product/Theme: {tema}
- Post concept: {melhor_ideia}
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
