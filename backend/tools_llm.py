def gerar_ideias_tool(state):

    prompt = f"""
Crie 3 ideias de post.

Plataforma: {state.get("plataforma")}
Tema: {state.get("tema")}
Objetivo: {state.get("objetivo")}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"ideias": response.choices[0].message.content}

def gerar_legenda_tool(state):

    prompt = f"""
Crie uma legenda para {state.get("plataforma")}.

Tema: {state.get("tema")}
Objetivo: {state.get("objetivo")}

Inclua:
- hook
- corpo
- CTA
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"legenda": response.choices[0].message.content}
