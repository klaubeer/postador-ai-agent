from llm import gerar_ideias_post

def gerar_ideias_tool(state):

    ideias = gerar_ideias_post(
        state["tema"],
        state["plataforma"],
        state["objetivo"]
    )

    return {"ideias": ideias}
