from typing import TypedDict
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    message: str
    resposta: str


def perguntar_objetivo(state: AgentState):

    return {
        "resposta": """Qual é o objetivo desse post?

Vender
Engajar
Educar
Inspirar
Entreter
"""
    }


def perguntar_plataforma(state: AgentState):

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


def gerar_resposta_final(state: AgentState):

    return {
        "resposta": f"Você disse: {state['message']}"
    }


builder = StateGraph(AgentState)

builder.add_node("objetivo", perguntar_objetivo)
builder.add_node("plataforma", perguntar_plataforma)
builder.add_node("final", gerar_resposta_final)

builder.set_entry_point("objetivo")

builder.add_edge("objetivo", "plataforma")
builder.add_edge("plataforma", "final")
builder.add_edge("final", END)

graph = builder.compile()


def agent_graph_chat(message):

    result = graph.invoke({
        "message": message
    })

    return result["resposta"]
