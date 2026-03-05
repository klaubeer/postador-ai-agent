import json
from backend.llm import llm


SYSTEM_PROMPT = """
Você é O Postador 🤖, um assistente que ajuda clientes a criar posts para redes sociais.

Seu objetivo é guiar o usuário na criação de um post.

Fluxo da conversa:

1. Descubra o objetivo do post
(vender, engajar, educar, inspirar, entreter)

2. Descubra a plataforma
Instagram, Facebook, TikTok, LinkedIn, X ou YouTube Shorts

3. Descubra o tema / produto / empresa / público

4. Quando tiver informação suficiente gere 3 ideias contendo:

🎯 Título
✍️ Legenda com CTA
🖼️ Sugestão de imagem
🏷️ Hashtags (se Instagram ou TikTok)

5. Peça para o usuário escolher uma ideia.

Se faltar informação, pergunte naturalmente.

Responda APENAS em JSON:

{
 "action": "ask_user | run_post_pipeline",
 "message": "mensagem para o usuário",
 "state_updates": {
   "objetivo": "...",
   "plataforma": "...",
   "tema": "...",
   "publico": "..."
 }
}
"""


def planner(user_input, state):

    prompt = f"""
{SYSTEM_PROMPT}

Estado atual:
{state}

Mensagem do usuário:
{user_input}
"""

    result = llm(prompt)

    try:
        decision = json.loads(result)
    except:
        decision = {
            "action": "ask_user",
            "message": "Pode me contar um pouco mais sobre o post que você quer criar?",
            "state_updates": {}
        }

    # atualiza state
    for k, v in decision.get("state_updates", {}).items():
        if v:
            state[k] = v

    return decision, state
