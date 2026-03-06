from backend.llm import llm


def generate_ideas(state):

    prompt = f"""
Crie 3 ideias curtas de post.

Produto/Tema: {state.get("tema")}
Plataforma: {state.get("plataforma")}
Público: {state.get("publico")}
Objetivo: {state.get("objetivo")}

Regras:
- usar o produto ou tema
- pensar no público
- máximo 20 palavras por ideia
- apenas lista numerada
- sem explicação
"""

    ideias = llm(prompt)

    if ideias:
        ideias = ideias.strip()

    state["ideias"] = ideias

    return state


def select_best_idea(state):

    prompt = f"""
Escolha a melhor ideia para viralizar.

Ideias:
{state.get("ideias")}

Regras:
- retorne apenas o texto da ideia escolhida
- sem explicação
"""

    melhor = llm(prompt)

    if melhor:
        melhor = melhor.strip()

    state["melhor_ideia"] = melhor

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

    state["legenda"] = legenda

    return state


def generate_image_prompt(state):

    prompt = f"""
Crie prompt curto para gerar imagem.

Produto/Tema: {state.get("tema")}
Ideia: {state.get("melhor_ideia")}
Público: {state.get("publico")}

Regras:
- máximo 15 palavras
- imagem deve mostrar o produto
- estilo visual claro
"""

    image_prompt = llm(prompt)

    if image_prompt:
        image_prompt = image_prompt.strip()

    state["image_prompt"] = image_prompt

    # ativa modo de aprovação de imagem
    state["awaiting_image_approval"] = True

    return state


def generate_hashtags(state):

    plataforma = state.get("plataforma")

    # hashtags só fazem sentido para essas plataformas
    if plataforma and plataforma.lower() not in ["instagram", "tiktok"]:
        state["hashtags"] = ""
        return state

    prompt = f"""
Crie até 5 hashtags para redes sociais.

Produto/Tema: {state.get("tema")}
Público: {state.get("publico")}

Retorne apenas palavras separadas por espaço.
"""

    hashtags = llm(prompt)

    if hashtags:

        hashtags = hashtags.replace("\n", " ").strip()

        tags = hashtags.split()

        # força #
        tags = [t if t.startswith("#") else f"#{t}" for t in tags]

        # máximo 5
        tags = tags[:5]

        hashtags = " ".join(tags)

    state["hashtags"] = hashtags

    return state


def format_post(state):

    ideia = state.get("melhor_ideia", "")
    legenda = state.get("legenda", "")
    hashtags = state.get("hashtags", "")
    image_prompt = state.get("image_prompt", "")
   
    state["post_final"] = f"""
🎯 Ideia
{ideia}

✍️ Legenda
{legenda}

🏷️ Hashtags
{hashtags}

🖼️ Prompt de imagem
{image_prompt}

Digite **gerar** para criar a imagem.
"""

    return state
