from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool


def node_inicio(state: AgentState):

    return {
        "resposta": """Qual é o objetivo desse post?

Vender
Engajar
Educar
Inspirar
Entreter
"""
    }


def node_plataforma(state: AgentState):

    return {
        "resposta": """Em qual plataforma será publicado?

Instagram
Facebook
TikTok
LinkedIn
X
YouTube Shorts
"""
    }


def node_tema(state: AgentState):

    return {"resposta": "Qual é o tema do post?"}


def node_gerar_ideias(state: AgentState):

    result = gerar_ideias_tool(state)

    return {
        "ideias": result["ideias"],
        "resposta": f"""
Aqui vão 3 ideias de post:

{result["ideias"]}

Qual você escolhe?
"""
    }


builder = StateGraph(AgentState)

builder.add_node("inicio", node_inicio)
builder.add_node("plataforma", node_plataforma)
builder.add_node("tema", node_tema)
builder.add_node("gerar_ideias", node_gerar_ideias)

builder.set_entry_point("inicio")

builder.add_edge("inicio", "plataforma")
builder.add_edge("plataforma", "tema")
builder.add_edge("tema", "gerar_ideias")
builder.add_edge("gerar_ideias", END)

graph = builder.compile()


def agent_graph_chat(message):

    result = graph.invoke({
        "message": message
    })

    return result["resposta"]
