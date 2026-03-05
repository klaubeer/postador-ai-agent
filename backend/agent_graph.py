from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool

# memória simples por sessão
sessions = {}


# -------------------------
# NODES
# -------------------------

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
    state["step"] = "fim"

    result = gerar_ideias_tool(state)

    return {
        "ideias": result["ideias"],
        "resposta": f"""
Aqui vão 3 ideias de post:

{result["ideias"]}

Qual você escolhe?
"""
    }


# -------------------------
# ROUTER
# -------------------------

def router(state: AgentState):

    step = state.get("step", "inicio")

    if step == "inicio":
        return "inicio"

    if step == "objetivo":
        return "objetivo"

    if step == "plataforma":
        return "plataforma"

    if step == "tema":
        return "tema"

    return END


# -------------------------
# LANGGRAPH
# -------------------------

builder = StateGraph(AgentState)

builder.add_node("inicio", node_inicio)
builder.add_node("objetivo", node_objetivo)
builder.add_node("plataforma", node_plataforma)
builder.add_node("tema", node_tema)

builder.set_entry_point("inicio")

builder.add_conditional_edges("inicio", router)
builder.add_conditional_edges("objetivo", router)
builder.add_conditional_edges("plataforma", router)
builder.add_conditional_edges("tema", router)

graph = builder.compile()


# -------------------------
# EXECUÇÃO DO AGENTE
# -------------------------

def agent_graph_chat(session_id, message):

    if session_id not in sessions:
        sessions[session_id] = {
            "session_id": session_id,
            "step": "inicio"
        }

    state = sessions[session_id]
    state["message"] = message

    result = graph.invoke(state)

    sessions[session_id] = result

    return result["resposta"]
