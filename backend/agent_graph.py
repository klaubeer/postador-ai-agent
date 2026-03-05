from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool

from openai import OpenAI
import json

client = OpenAI()

# memória simples por sessão
sessions = {}


# -------------------------
# NODE 1 — interpretar mensagem
# -------------------------

def node_interpret_message(state: AgentState):

    message = state.get("message", "")

    prompt = f"""
Extraia informações da mensagem do usuário.

Mensagem:
{message}

Retorne JSON com os campos abaixo se existirem:

objetivo: vender | educar | engajar | inspirar | entreter
plataforma: instagram | facebook | tiktok | linkedin | x | youtube
tema: texto livre

Se não souber algum campo, retorne null.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except:
        data = {}

    if data.get("objetivo"):
        state["objetivo"] = data["objetivo"]

    if data.get("plataforma"):
        state["plataforma"] = data["plataforma"]

    if data.get("tema"):
        state["tema"] = data["tema"]

    return state


# -------------------------
# NODE 2 — decidir próxima ação
# -------------------------

def node_decide_next(state: AgentState):

    if not state.get("plataforma"):

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

    if not state.get("objetivo"):

        return {
            "resposta": """Qual é o objetivo do post?

Vender
Educar
Engajar
Inspirar
Entreter
"""
        }

    if not state.get("tema"):

        return {
            "resposta": "Qual é o tema do post?"
        }

    state["next"] = "gerar_ideias"

    return state


# -------------------------
# NODE 3 — gerar ideias
# -------------------------

def node_gerar_ideias(state: AgentState):

    result = gerar_ideias_tool(state)

    ideias = result.get("ideias", "")

    return {
        "resposta": f"""
Aqui vão 3 ideias de post:

{ideias}

Qual você prefere?
"""
    }


# -------------------------
# ROUTER
# -------------------------

def router(state: AgentState):

    if state.get("next") == "gerar_ideias":
        return "gerar_ideias"

    return "decide_next"


# -------------------------
# LANGGRAPH
# -------------------------

builder = StateGraph(AgentState)

builder.add_node("interpret", node_interpret_message)
builder.add_node("decide_next", node_decide_next)
builder.add_node("gerar_ideias", node_gerar_ideias)

builder.set_entry_point("interpret")

builder.add_edge("interpret", "decide_next")

builder.add_conditional_edges(
    "decide_next",
    router
)

builder.add_edge("gerar_ideias", END)

graph = builder.compile()


# -------------------------
# FUNÇÃO USADA PELA API
# -------------------------

def agent_graph_chat(session_id, message):

    if session_id not in sessions:
        sessions[session_id] = {
            "session_id": session_id
        }

    state = sessions[session_id]
    state["message"] = message

    result = graph.invoke(state)

    # atualizar memória
    sessions[session_id] = {**state, **result}

    return result.get("resposta", "Não consegui gerar resposta.")
