from openai import OpenAI

client = OpenAI()


def gerar_ideias_tool(state):

    prompt = f"""
Crie 3 ideias de post para redes sociais.

Plataforma: {state.get("plataforma")}
Tema: {state.get("tema")}
Objetivo: {state.get("objetivo")}

As ideias devem conter:
1. Título
2. Descrição breve
3. Sugestão visual
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um especialista em social media."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "ideias": response.choices[0].message.content
    }


def gerar_legenda_tool(state):

    prompt = f"""
Crie uma legenda para redes sociais.

Plataforma: {state.get("plataforma")}
Tema: {state.get("tema")}
Objetivo: {state.get("objetivo")}

A legenda deve conter:
- Hook inicial
- Conteúdo principal
- CTA
- 5 hashtags relevantes
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um especialista em marketing digital."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "legenda": response.choices[0].message.content
    }
