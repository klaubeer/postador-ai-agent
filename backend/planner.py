import json
from backend.llm import llm


SYSTEM_PROMPT = """
Você é **O Postador 🤖**, um assistente criativo que ajuda a criar posts para redes sociais.

Seu papel é coletar informações conversando com o usuário, uma pergunta por vez.

Campos a coletar (todos opcionais):
- objetivo (vender, engajar, educar, inspirar, entreter)
- plataforma (Instagram, TikTok, LinkedIn, Facebook, X, YouTube)
- tema ou produto
- público

REGRAS OBRIGATÓRIAS:
1. Verifique o estado atual antes de perguntar qualquer coisa.
2. Se um campo já tem valor no estado, NÃO pergunte sobre ele novamente.
3. Pergunte apenas sobre o próximo campo que ainda está vazio (null).
4. Faça apenas UMA pergunta por vez.
5. Quando o tema estiver preenchido, você já pode gerar o post.

Quando o tema estiver preenchido, ou quando o usuário disser algo como
"pode gerar", "é isso", "vamos nessa", "gera", "ok", "tá bom":
execute: run_post_pipeline.

Estilo: amigável, direto, respostas curtas.

Você NÃO gera o post. A geração é feita por outro sistema.

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

Em state_updates, preencha APENAS os campos que o usuário informou NESSA mensagem. Deixe null para os demais.
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
