from openai import OpenAI

client = OpenAI()

def gerar_ideias_post(tema, plataforma, objetivo):

    prompt = f"""
Você é um especialista em marketing digital.

Crie 3 ideias de posts para:

Tema: {tema}
Plataforma: {plataforma}
Objetivo: {objetivo}

Cada ideia deve ter:
- Título
- Tipo de conteúdo
- Breve explicação

Responda numerado (1,2,3).
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você é um estrategista de conteúdo."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
