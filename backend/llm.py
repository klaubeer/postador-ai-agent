# backend/llm.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_ideias_post(tema, plataforma, objetivo):

    prompt = f"""
Você é um estrategista de marketing digital especialista em redes sociais.

Crie 3 ideias de posts para:

Tema: {tema}
Plataforma: {plataforma}
Objetivo: {objetivo}

Cada ideia deve ter:

1️⃣ Título do post
✍️ Breve descrição do conteúdo
🎯 Tipo de conteúdo (dica, curiosidade, história, tutorial etc)

Se a plataforma for Instagram ou TikTok, inclua hashtags.

Responda numerado (1, 2, 3).
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você cria ideias virais para redes sociais."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return response.choices[0].message.content

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "Você cria ideias virais para redes sociais."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.8
)

print("TOKENS USADOS:", response.usage)

return response.choices[0].message.content
