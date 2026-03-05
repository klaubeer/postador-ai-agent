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
- máximo 12 palavras por ideia
- apenas lista numerada
- sem explicação
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
- retorne apenas o texto da ideia escolhida
- sem explicação
"""

    melhor = llm(prompt)

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

    state["image_prompt"] = image_prompt

    return state


def generate_hashtags(state):

    plataforma = state.get("plataforma")

    if plataforma and plataforma.lower() not in ["instagram", "tiktok"]:
        state["hashtags"] = ""
        return state

    prompt = f"""
Crie hashtags para redes sociais.

Produto/Tema: {state.get("tema")}
Público: {state.get("publico")}
Plataforma: {plataforma}

Regras:
- máximo 5 hashtags
- incluir hashtag do produto
- apenas hashtags
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

🖼️ Prompt de imagem
{state.get("image_prompt")}

Digite **gerar imagem** para criar a imagem.
"""
"""

    return state
