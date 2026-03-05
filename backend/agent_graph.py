from langgraph.graph import StateGraph, END
from state import AgentState
from tools_llm import gerar_ideias_tool, gerar_legenda_tool
from rag.retriever import search

from openai import OpenAI
import json

client = OpenAI()

sessions = {}

# -------------------------
# EXTRACT BRIEFING (LLM)
# -------------------------

def node_extract_briefing(state: AgentState):

    message = state.get("message")

    briefing = {
        "objetivo": state.get("objetivo"),
        "produto": state.get("produto"),
        "publico": state.get("publico"),
        "rede_social": state.get("rede_social")
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You extract social media briefing info.

Return JSON only.

Fields:

objetivo
produto
publico
rede_social

If not mentioned return null.

Examples:

User: I want to sell mugs on Instagram

{
 "objetivo":"vender",
 "produto":"canecas",
 "publico":null,
 "rede_social":"instagram"
}

User: promoting my AI course to developers on linkedin

{
 "objetivo":"vender",
 "produto":"curso de IA",
 "publico":"desenvolvedores",
 "rede_social":"linkedin"
}
"""
            },
            {
                "role": "user",
                "content": f"""
Current briefing:

{briefing}

User message:

{message}

Update the briefing.
"""
            }
        ]
    )

    try:
        data = json.loads(response.choices[0].message.content)
    except:
        return state

    for k, v in data.items():
        if v:
            state[k] = v

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
• sell
• engage
• educate
• build authority
• promote product
"""
        }

    return {
        "resposta": """
Qual é o objetivo do post?

Exemplos:
• vender
• engajar
• educar
• gerar autoridade
• divulgar produto
"""
    }


# -------------------------
# MISSING INFO
# -------------------------

def node_missing_info(state: AgentState):

    lang = state.get("language", "pt")

    missing = []

    if not state.get("produto"):
        missing.append("produto")

    if not state.get("publico"):
        missing.append("público")

    if not state.get("rede_social"):
        missing.append("rede social")

    if not missing:
        return state

    if lang == "en":

        pergunta = f"""
Great. I understood the goal is **{state.get("objetivo")}**.

To generate the post I just need:

{", ".join(missing)}

You can answer everything in one sentence.
"""

    else:

        pergunta = f"""
Perfeito. Entendi que o objetivo é **{state.get("objetivo")}**.

Para criar o post preciso só de mais algumas coisas:

{", ".join(missing)}

Você pode responder tudo em uma frase se quiser.
"""

    return {"resposta": pergunta}


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
# ROUTERS
# -------------------------

def router_briefing(state: AgentState):

    if not state.get("objetivo"):
        return "perguntar_objetivo"

    if not state.get("produto") or not state.get("publico") or not state.get("rede_social"):
        return "missing_info"

    return "planner"


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

builder.add_node("extract_briefing", node_extract_briefing)
builder.add_node("rag", node_rag)

builder.add_node("perguntar_objetivo", node_perguntar_objetivo)
builder.add_node("missing_info", node_missing_info)

builder.add_node("planner", node_planner)
builder.add_node("gerar_ideias", node_gerar_ideias)
builder.add_node("gerar_legenda", node_gerar_legenda)
builder.add_node("conversa", node_conversa)

builder.set_entry_point("extract_briefing")

builder.add_edge("extract_briefing", "rag")

builder.add_conditional_edges(
    "rag",
    router_briefing
)

builder.add_conditional_edges(
    "planner",
    router
)

builder.add_edge("missing_info", END)
builder.add_edge("perguntar_objetivo", END)

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

I help you create social media content.

Please, tell me what would you like to post.
"""

        else:

            mensagem_boas_vindas = """
Olá! Eu sou o Postador 🤖

Vou te ajudar a criar conteúdo para redes sociais.

Me diga, o que você quer postar?
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
