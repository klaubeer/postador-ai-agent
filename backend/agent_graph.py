from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool, gerar_legenda_tool

from openai import OpenAI
import json

client = OpenAI()

# memória simples por sessão
sessions = {}

# -------------------------
# CAPTURAR OBJETIVO
# -------------------------

def node_capturar_objetivo(state: AgentState):

    mensagem = state.get("message", "").lower()

    if not state.get("objetivo"):

        objetivos_validos = [
            "vender",
            "engajar",
            "educar",
            "autoridade",
            "divulgar"
        ]

        for obj in objetivos_validos:
            if obj in mensagem:
                state["objetivo"] = obj
                break

    return state


# -------------------------
# PERGUNTAR OBJETIVO
# -------------------------

def node_perguntar_objetivo(state: AgentState):

    return {
        "resposta": """
Qual é o objetivo do post?

Você pode responder algo como:
(vender, engajar, educar, gerar autoridade, divulgar produto)

Qual é o seu objetivo?
"""
    }


# -------------------------
# PLANNER (LLM decide intenção)
# -------------------------

def node_planner(state: AgentState):

    history = state.get("history", [])[-20:]

    messages = [
        {
            "role": "system",
            "content": """
Você é um assistente de social media.

O objetivo do post é: """ + str(state.get("objetivo", "")) + """

Analise a conversa e identifique a intenção do usuário.

Possíveis intenções:

gerar_ideias
gerar_legenda
conversa

Responda apenas JSON:

{ "intent": "..." }
"""
        }
    ] + history

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

    ideias = gerar_ideias_tool(state)

    return {
    "ideias": ideias["ideias"]
}




# -------------------------
# EXECUTOR LEGENDA
# -------------------------

def node_gerar_legenda(state: AgentState):

    legenda = gerar_legenda_tool(state)

    resposta = f"""
Aqui vão 3 ideias de post:

{state.get("ideias")}

---

Legenda sugerida:

{legenda["legenda"]}
"""

    return {
        "resposta": resposta
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
# ROUTER INICIAL
# -------------------------

def router_inicio(state: AgentState):

    if not state.get("objetivo"):
        return "perguntar_objetivo"

    return "planner"


# -------------------------
# ROUTER PRINCIPAL
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

builder.add_node("capturar_objetivo", node_capturar_objetivo)
builder.add_node("perguntar_objetivo", node_perguntar_objetivo)

builder.add_node("planner", node_planner)
builder.add_node("gerar_ideias", node_gerar_ideias)
builder.add_node("gerar_legenda", node_gerar_legenda)
builder.add_node("conversa", node_conversa)

builder.set_entry_point("capturar_objetivo")

builder.add_conditional_edges(
    "capturar_objetivo",
    router_inicio
)

builder.add_conditional_edges(
    "planner",
    router
)

builder.add_edge("perguntar_objetivo", END)
builder.add_edge("gerar_ideias", "gerar_legenda")
builder.add_edge("gerar_legenda", END)
builder.add_edge("conversa", END)

graph = builder.compile()


# -------------------------
# FUNÇÃO USADA PELO FASTAPI
# -------------------------

def agent_graph_chat(session_id, message):

    if session_id not in sessions:

        mensagem_boas_vindas = """
Olá! Eu sou o Postador 🤖

Posso ajudar você a criar conteúdo para redes sociais.

Antes de começarmos:

Qual é o objetivo do post?

(vender, engajar, educar, gerar autoridade, divulgar produto)
"""

        sessions[session_id] = {
            "session_id": session_id,
            "history": [
                {
                    "role": "assistant",
                    "content": mensagem_boas_vindas
                }
            ],
            "objetivo": None
        }

        return mensagem_boas_vindas

    state = sessions[session_id]

    state["history"].append({
        "role": "user",
        "content": message
    })

    state["message"] = message

    result = graph.invoke(state)

    resposta = result.get("resposta", "Não consegui gerar resposta.")

    state["history"].append({
        "role": "assistant",
        "content": resposta
    })

    sessions[session_id] = state

    return resposta
