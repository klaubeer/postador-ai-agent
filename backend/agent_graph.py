from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool, gerar_legenda_tool
from rag.retriever import search

from openai import OpenAI
import json

client = OpenAI()

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
# CAPTURAR BRIEFING
# -------------------------

def node_capturar_briefing(state: AgentState):

    mensagem = state.get("message", "").lower()

    if not state.get("produto"):
        state["produto"] = mensagem
        return state

    if not state.get("publico"):
        state["publico"] = mensagem
        return state

    if not state.get("rede_social"):
        state["rede_social"] = mensagem
        return state

    return state


# -------------------------
# RAG
# -------------------------

def node_rag(state: AgentState):

    query = state.get("message", "")
    contexto = search(query)

    state["contexto_rag"] = contexto

    return state


# -------------------------
# PERGUNTAR OBJETIVO
# -------------------------

def node_perguntar_objetivo(state: AgentState):

    lang = state.get("language", "pt")

    if lang == "en":
        return {
            "resposta": """
What is the goal of the post?

Examples:
(sell, engage, educate, authority, promote product)
"""
        }

    return {
        "resposta": """
Qual é o objetivo do post?

Você pode responder algo como:
(vender, engajar, educar, gerar autoridade, divulgar produto)
"""
    }


# -------------------------
# PERGUNTAR PRODUTO
# -------------------------

def node_perguntar_produto(state: AgentState):

    lang = state.get("language", "pt")

    if lang == "en":
        return {
            "resposta": "What product or service do you want to promote?"
        }

    return {
        "resposta": "Qual produto ou serviço você quer divulgar?"
    }


# -------------------------
# PERGUNTAR PUBLICO
# -------------------------

def node_perguntar_publico(state: AgentState):

    lang = state.get("language", "pt")

    if lang == "en":
        return {
            "resposta": "Who is the target audience?"
        }

    return {
        "resposta": "Quem é o público-alvo?"
    }


# -------------------------
# PERGUNTAR REDE SOCIAL
# -------------------------

def node_perguntar_rede(state: AgentState):

    lang = state.get("language", "pt")

    if lang == "en":
        return {
            "resposta": "Which social network will this post be for?"
        }

    return {
        "resposta": "Para qual rede social é o post? (Instagram, LinkedIn, etc)"
    }


# -------------------------
# PLANNER
# -------------------------

def node_planner(state: AgentState):

    history = state.get("history", [])[-20:]
    contexto = state.get("contexto_rag", "")
    lang = state.get("language", "pt")

    messages = [
        {
            "role": "system",
            "content": f"""
You are a social media assistant.

Respond in {lang}

CONTEXT:

{contexto}

Identify user intent.

Possible intents:

gerar_ideias
gerar_legenda
conversa

Return JSON only.

{{ "intent": "..." }}
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

    state["intent"] = data.get("intent")

    return state


# -------------------------
# IDEIAS
# -------------------------

def node_gerar_ideias(state: AgentState):

    ideias = gerar_ideias_tool(state)

    return {
        "ideias": ideias["ideias"]
    }


# -------------------------
# LEGENDA
# -------------------------

def node_gerar_legenda(state: AgentState):

    legenda = gerar_legenda_tool(state)

    resposta = f"""
Aqui vão algumas ideias de post:

{state.get("ideias")}

---

Legenda sugerida:

{legenda["legenda"]}
"""

    return {
        "resposta": resposta
    }


# -------------------------
# CONVERSA
# -------------------------

def node_conversa(state: AgentState):

    contexto = state.get("contexto_rag", "")
    pergunta = state.get("message", "")
    history = state.get("history", [])
    lang = state.get("language", "pt")

    messages = [
        {
            "role": "system",
            "content": f"""
You are Postador, a social media assistant.

Always respond in {lang}.
"""
        },
        {
            "role": "user",
            "content": f"""
CONTEXT:
{contexto}

USER QUESTION:
{pergunta}
"""
        }
    ] + history

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
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

    if not state.get("produto"):
        return "perguntar_produto"

    if not state.get("publico"):
        return "perguntar_publico"

    if not state.get("rede_social"):
        return "perguntar_rede"

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
builder.add_node("capturar_briefing", node_capturar_briefing)

builder.add_node("rag", node_rag)

builder.add_node("perguntar_objetivo", node_perguntar_objetivo)
builder.add_node("perguntar_produto", node_perguntar_produto)
builder.add_node("perguntar_publico", node_perguntar_publico)
builder.add_node("perguntar_rede", node_perguntar_rede)

builder.add_node("planner", node_planner)
builder.add_node("gerar_ideias", node_gerar_ideias)
builder.add_node("gerar_legenda", node_gerar_legenda)
builder.add_node("conversa", node_conversa)

builder.set_entry_point("capturar_objetivo")

builder.add_edge("capturar_objetivo", "capturar_briefing")
builder.add_edge("capturar_briefing", "rag")

builder.add_conditional_edges(
    "rag",
    router_inicio
)

builder.add_conditional_edges(
    "planner",
    router
)

builder.add_edge("perguntar_objetivo", END)
builder.add_edge("perguntar_produto", END)
builder.add_edge("perguntar_publico", END)
builder.add_edge("perguntar_rede", END)

builder.add_edge("gerar_ideias", "gerar_legenda")
builder.add_edge("gerar_legenda", END)
builder.add_edge("conversa", END)

graph = builder.compile()


# -------------------------
# CHAT
# -------------------------

def agent_graph_chat(session_id, message, language="pt"):

    if session_id not in sessions:

        if language == "en":
            mensagem_boas_vindas = """
Hello! I'm The Postador 🤖

I can help you create social media content.

First:

What is the goal of your post?
"""
        else:
            mensagem_boas_vindas = """
Olá! Eu sou o Postador 🤖

Posso ajudar você a criar conteúdo para redes sociais.

Qual é o objetivo do post?
"""

        sessions[session_id] = {
            "session_id": session_id,
            "history": [
                {"role": "assistant", "content": mensagem_boas_vindas}
            ],
            "objetivo": None,
            "produto": None,
            "publico": None,
            "rede_social": None,
            "language": language
        }

        return mensagem_boas_vindas

    state = sessions[session_id]

    state["language"] = language

    state["history"].append({
        "role": "user",
        "content": message
    })

    state["message"] = message

    state = graph.invoke(state)

    resposta = state.get("resposta", "Erro ao gerar resposta.")

    state["history"].append({
        "role": "assistant",
        "content": resposta
    })

    sessions[session_id] = state

    return resposta
