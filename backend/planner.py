import json
from backend.llm import llm


SYSTEM_PROMPT = """
Você é **O Postador 🤖**, um super assistente criativo que ajuda pessoas a criar posts para redes sociais.

Seu papel é **conversar com o usuário e coletar informações** antes de gerar o post.

Informações úteis (todas opcionais):
- objetivo do post
- plataforma
- tema ou produto
- público

Estilo:
- amigável
- criativo
- direto
- respostas curtas

Fluxo natural da conversa:

1. Descubra o objetivo do post (vender, engajar, educar, inspirar ou entreter).
2. Pergunte em qual rede social será publicado.
3. Descubra o tema ou produto.
4. Entenda quem é o público.

Você NÃO deve gerar o post aqui.
A geração será feita depois por outro sistema.

Quando houver contexto suficiente ou quando o usuário disser algo como:
"pode gerar", "é isso", "vamos nessa", etc

execute: run_post_pipeline.

Responda SOMENTE em JSON:

{
 "action": "ask_user | run_post_pipeline",
 "message": "mensagem para o usuário",
 "state_updates": {
   "objetivo": null,
   "plataforma": null,
   "tema": null,
   "publico": null
 }
}
"""


def extract_json(text: str):

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception:

        print("\n❌ LLM retornou JSON inválido:")
        print(text)
        print("--------------------------------------------------\n")

        return {
            "action": "ask_user",
            "message": "Desculpe, houve um erro. Pode repetir?",
            "state_updates": {}
        }


def planner(user_input: str, state: dict):

    prompt = f"""
Estado atual da conversa:

objetivo: {state.get("objetivo")}
plataforma: {state.get("plataforma")}
tema: {state.get("tema")}
publico: {state.get("publico")}

Mensagem do usuário:
{user_input}
"""

    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

    print("\n========== PROMPT ENVIADO AO LLM ==========")
    print(full_prompt)
    print("===========================================\n")

    result = llm(full_prompt)

    print("\n========== RESPOSTA BRUTA DO LLM ==========")
    print(result)
    print("===========================================\n")

    decision = extract_json(result)

    print("\n========== DECISÃO PARSEADA ==========")
    print(decision)
    print("======================================\n")

    # Atualiza estado da conversa
    updates = decision.get("state_updates", {})

    for key, value in updates.items():
        if value:
            state[key] = value

    return {
        "action": decision.get("action", "ask_user"),
        "message": decision.get("message", "Ok."),
        "state": state
    }
