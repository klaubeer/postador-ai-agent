from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool, gerar_legenda_tool

from openai import OpenAI
import json

client = OpenAI()

# memória simples por sessão
sessions = {}


# -------------------------
# PLANNER (LLM decide intenção)
# -------------------------

def node_planner(state: AgentState):

    history = state.get("history", [])

    messages = history + [
        {
            "role": "system",
            "content": """
Você é um assistente de social media.

Analise a conversa e identifique a intenção do usuário.

Possíveis intenções:

gerar_ideias
gerar_legenda
conversa

Responda apenas JSON:

{ "intent": "..." }
"""
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except:
        data = {"intent": "conversa"}

    state["intent"] = data.get("intent", "conversa")

    return state


# -------------------------
# EXECUTOR IDEIAS
# -------------------------

def node_gerar_ideias(state: AgentState):

    result = gerar_ideias_tool(state)

    return {
        "resposta": f"""
Aqui vão 3 ideias de post:

{result["ideias"]}
"""
    }


# -------------------------
# EXECUTOR LEGENDA
# -------------------------

def node_gerar_legenda(state: AgentState):

    result = gerar_legenda_tool(state)

    return {
        "resposta": result["legenda"]
    }


# -------------------------
# CONVERSA NORMAL
# -------------------------

def node_conversa(state: AgentState):

    history = state.get("history", [])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente de social media."}
        ] + history
    )

    return {
        "resposta": response.choices[0].message.content
    }


# -------------------------
# ROUTER
# -------------------------

def router(state: AgentState):

    intent = state.get("intent")

    if intent == "gerar_ideias":
        return "gerar_ideias"

    if intent == "gerar_legenda":
        return "gerar_legenda"

    return "conversa"


# -------------------------
# LANGGRAPH
# -------------------------

builder = StateGraph(AgentState)

builder.add_node("planner", node_planner)
builder.add_node("gerar_ideias", node_gerar_ideias)
builder.add_node("gerar_legenda", node_gerar_legenda)
builder.add_node("conversa", node_conversa)

builder.set_entry_point("planner")

builder.add_conditional_edges(
    "planner",
    router
)

builder.add_edge("gerar_ideias", END)
builder.add_edge("gerar_legenda", END)
builder.add_edge("conversa", END)

graph = builder.compile()


# -------------------------
# FUNÇÃO USADA PELO FASTAPI
# -------------------------

def agent_graph_chat(session_id, message):

    if session_id not in sessions:
        sessions[session_id] = {
            "session_id": session_id,
            "history": []
        }

    state = sessions[session_id]

    # adicionar mensagem do usuário
    state["history"].append({
        "role": "user",
        "content": message
    })

    state["message"] = message

    result = graph.invoke(state)

    resposta = result.get("resposta", "Não consegui gerar resposta.")

    # salvar resposta na memória
    state["history"].append({
        "role": "assistant",
        "content": resposta
    })

    sessions[session_id] = state

    return resposta
