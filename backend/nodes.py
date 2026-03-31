from backend.llm import llm


PLATFORM_STYLE = {
    "instagram": "Linguagem leve, emojis, hashtags, visual para carrossel ou reels.",
    "tiktok": "Criativo, vídeos curtos, tendências, hashtags fortes.",
    "facebook": "Explicativo, amigável, com links e engajamento.",
    "linkedin": "Profissional, direto, com autoridade e storytelling.",
    "x": "Textos curtos e impactantes, sem exagero de hashtags.",
    "youtube": "Visual forte, gancho rápido e linguagem envolvente.",
}

VISUAL_STYLES = {
    "1": "Realismo — elegante, profissional, realista, sóbrio, bem iluminado",
    "2": "Visão Futurista — moderno, limpo, tecnológico, futurista, claro",
    "3": "Surreal — colorido, onírico, exagerado, lúdico, criativo",
    "4": "Distopia — sombrio, glitch, neon, distópico",
}


def generate_ideas(state):
    """Gera 3 ideias de post detalhadas para o usuário escolher."""

    tema = state.get("tema", "")
    plataforma = state.get("plataforma", "Instagram")
    objetivo = state.get("objetivo", "engajar")
    publico = state.get("publico", "público geral")
    detalhes = state.get("detalhes", "")

    plat_key = plataforma.lower().replace("twitter", "x").replace("youtube shorts", "youtube")
    style_guide = PLATFORM_STYLE.get(plat_key, "Adapte ao tom da plataforma.")

    prompt = f"""Você é um social media expert criativo.

CONTEXTO:
- Tema/Produto: {tema}
- Plataforma: {plataforma}
- Objetivo: {objetivo}
- Público-alvo: {publico}
- Detalhes extras: {detalhes or 'nenhum'}
- Estilo da plataforma: {style_guide}

Sugira 3 ideias de post. Cada ideia deve conter:

IDEIA 1:
🎯 Título: [título criativo + tipo de conteúdo (carrossel, reels, post estático, vídeo curto, etc)]
✍️ Legenda: [legenda envolvente com CTA, adequada para {plataforma}]
🖼️ Visual: [sugestão do que mostrar na imagem/vídeo]
🏷️ Hashtags: [5 hashtags relevantes separadas por espaço]

IDEIA 2:
(mesmo formato)

IDEIA 3:
(mesmo formato)

Regras:
- Cada ideia deve ter uma abordagem DIFERENTE
- Adapte ao público {publico} e ao objetivo de {objetivo}
- Seja criativo e prático
- Retorne EXATAMENTE no formato acima"""

    result = llm(prompt, nome="generate-ideas")
    state["ideias_raw"] = result.strip()

    return state


def generate_final_post(state):
    """Gera o post final com base na ideia escolhida e estilo visual."""

    ideia_escolhida = state.get("ideia_escolhida", "")
    plataforma = state.get("plataforma", "Instagram")
    publico = state.get("publico", "público geral")
    estilo_visual = state.get("estilo_visual", "1")
    tema = state.get("tema", "")

    style_desc = VISUAL_STYLES.get(str(estilo_visual), VISUAL_STYLES["1"])

    prompt = f"""Você é um social media expert.

Com base na ideia de post abaixo, gere o conteúdo FINAL para publicação.

IDEIA ESCOLHIDA:
{ideia_escolhida}

CONTEXTO:
- Plataforma: {plataforma}
- Público: {publico}
- Tema: {tema}
- Estilo visual escolhido: {style_desc}

Entregue EXATAMENTE neste formato:

LEGENDA:
[Legenda final polida, envolvente, com CTA. Pronta para copiar e colar na {plataforma}.]

HASHTAGS:
[5-8 hashtags relevantes separadas por espaço]

DESCRICAO_IMAGEM:
[Descrição visual detalhada para gerar a imagem com IA. Descreva a cena, composição, iluminação. NÃO repita o estilo visual aqui — ele será aplicado automaticamente. Máximo 2 frases em português.]"""

    result = llm(prompt, nome="generate-final-post")

    # parse
    legenda = ""
    hashtags = ""
    descricao_imagem = ""

    sections = {}
    current_section = None
    current_lines = []

    for line in result.split("\n"):
        stripped = line.strip()

        for label, key in [("LEGENDA:", "legenda"), ("HASHTAGS:", "hashtags"), ("DESCRICAO_IMAGEM:", "descricao_imagem")]:
            if stripped.startswith(label):
                if current_section:
                    sections[current_section] = "\n".join(current_lines).strip()
                current_section = key
                current_lines = []
                rest = stripped.replace(label, "").strip()
                if rest:
                    current_lines.append(rest)
                break
        else:
            if current_section:
                current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    legenda = sections.get("legenda", "")
    hashtags = sections.get("hashtags", "")
    descricao_imagem = sections.get("descricao_imagem", "")

    # garante formato hashtags
    if hashtags:
        tags = hashtags.replace("\n", " ").replace(",", " ").split()
        tags = [t if t.startswith("#") else f"#{t}" for t in tags if t]
        hashtags = " ".join(tags[:8])

    state["legenda"] = legenda
    state["hashtags"] = hashtags
    state["descricao_imagem"] = descricao_imagem

    return state


def generate_image_prompt(state):
    """Converte a descrição visual + estilo em prompt de IA para imagem."""

    descricao = state.get("descricao_imagem", "")
    estilo_visual = state.get("estilo_visual", "1")

    style_desc = VISUAL_STYLES.get(str(estilo_visual), VISUAL_STYLES["1"])

    prompt = f"""Write a short image prompt for FLUX AI generator.

Scene: {descricao}
Style: {style_desc}

Rules:
- English only
- MAX 25 words — be concise and visual
- Focus on ONE clear scene, not multiple
- No text in the image
- Return ONLY the prompt"""

    image_prompt = llm(prompt, nome="generate-image-prompt")

    if image_prompt:
        image_prompt = image_prompt.strip().strip('"').strip("'")

    state["image_prompt"] = image_prompt or ""

    return state
