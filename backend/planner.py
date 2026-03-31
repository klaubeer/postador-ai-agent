import json
from backend.llm import llm_chat


SYSTEM_PROMPT = """Você é o Postador, um assistente criativo que ajuda a criar posts para redes sociais.

Seu objetivo é entender o que o usuário quer e coletar contexto de forma natural, conversando — sem parecer um formulário.

## Informações que você precisa coletar (extraia do que o usuário diz, não pergunte uma por uma):
- tema: produto, serviço ou assunto do post
- plataforma: onde vai postar (Instagram, TikTok, LinkedIn, etc)
- objetivo: vender, engajar, educar, inspirar, entreter
- publico: para quem é o post
- detalhes: qualquer informação extra relevante (tom, estilo, promoção, etc)

## Regras:
1. Seja amigável, direto e criativo. Respostas curtas.
2. Extraia o máximo de informações implícitas da mensagem do usuário.
3. Se o usuário disser "quero vender meus bolos no Instagram", você já tem tema, plataforma e objetivo — não pergunte de novo.
4. Só pergunte o que realmente falta e é importante. O campo "tema" é obrigatório. Os outros são opcionais.
5. Quando tiver pelo menos o tema, e o usuário parecer pronto (ou disser "gera", "pode fazer", "manda", "vai", "ok"), acione o pipeline.
6. Você NÃO gera o post. Outro sistema faz isso.
7. Nunca repita informações que o usuário já deu.

## Formato de resposta (JSON obrigatório):
{
  "action": "ask_user" ou "run_post_pipeline",
  "message": "sua mensagem para o usuário",
  "state_updates": {
    "tema": null,
    "plataforma": null,
    "objetivo": null,
    "publico": null,
    "detalhes": null
  }
}

Em state_updates, preencha APENAS campos que o usuário informou. Deixe null os demais."""


def planner(messages: list, state: dict, session_id: str = None) -> dict:

    # monta contexto do estado atual
    state_context = "\n".join(
        f"- {k}: {v}" for k, v in state.items()
        if v and k in ("tema", "plataforma", "objetivo", "publico", "detalhes")
    )

    context_msg = "Estado atual da conversa:\n"
    if state_context:
        context_msg += state_context
    else:
        context_msg += "(nenhuma informação coletada ainda)"

    # injeta contexto como mensagem de sistema auxiliar
    full_messages = [{"role": "system", "content": context_msg}] + messages

    result = llm_chat(
        messages=full_messages,
        system=SYSTEM_PROMPT,
        session_id=session_id,
        json_mode=True,
        nome="planner"
    )

    try:
        decision = json.loads(result)
    except json.JSONDecodeError:
        print(f"[PLANNER] JSON inválido: {result}")
        decision = {
            "action": "ask_user",
            "message": "Desculpe, pode repetir?",
            "state_updates": {}
        }

    # atualiza estado
    updates = decision.get("state_updates", {})
    for key, value in updates.items():
        if value:
            state[key] = value

    return {
        "action": decision.get("action", "ask_user"),
        "message": decision.get("message", "Como posso ajudar?"),
        "state": state
    }
