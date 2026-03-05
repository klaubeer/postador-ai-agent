from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool

# memória simples por sessão
sessions = {}


def node_inicio(state: AgentState):

    state["step"] = "objetivo"

    return {
        "resposta": """Qual é o objetivo desse post?

Vender
Engajar
Educar
Inspirar
Entreter
"""
    }


def node_objetivo(state: AgentState):

    state["objetivo"] = state["message"]
    state["step"] = "plataforma"

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


def node_plataforma(state: AgentState):

    state["plataforma"] = state["message"]
    state["step"] = "tema"

    return {"resposta": "Qual é o tema do post?"}


def node_tema(state: AgentState):

    state["tema"] = state["message"]
    state["step"] = "ideias"

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
builder.add_node("objetivo", node_objetivo)
builder.add_node("plataforma", node_plataforma)
builder.add_node("tema", node_tema)

builder.set_entry_point("inicio")

builder.add_edge("inicio", "objetivo")
builder.add_edge("objetivo", "plataforma")
builder.add_edge("plataforma", "tema")
builder.add_edge("tema", END)

graph = builder.compile()


def agent_graph_chat(session_id, message):

    # cria sessão se não existir
    if session_id not in sessions:
        sessions[session_id] = {"step": "inicio"}

    state = sessions[session_id]
    state["message"] = message

    step = state["step"]

    if step == "inicio":
        result = node_inicio(state)

    elif step == "objetivo":
        result = node_objetivo(state)

    elif step == "plataforma":
        result = node_plataforma(state)

    elif step == "tema":
        result = node_tema(state)

    else:
        result = {"resposta": "Fluxo finalizado. Digite 'novo post'."}

    sessions[session_id] = state

    return result["resposta"]
