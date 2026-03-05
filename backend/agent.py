from memory import get_session
from tools import gerador_imagem
from llm import gerar_ideias_post


def agent_chat(session_id, message):

    session = get_session(session_id)

    # STEP 1 — INÍCIO
    if session["step"] == "inicio":
        session["step"] = "objetivo"

        return """Qual é o objetivo desse post?

Vender
Engajar
Educar
Inspirar
Entreter
"""

    # STEP 2 — OBJETIVO
    if session["step"] == "objetivo":
        session["objetivo"] = message
        session["step"] = "plataforma"

        return """Em qual plataforma será publicado?

Instagram
Facebook
TikTok
LinkedIn
X
YouTube Shorts
"""

    # STEP 3 — PLATAFORMA
    if session["step"] == "plataforma":
        session["plataforma"] = message
        session["step"] = "tema"

        return "Qual é o tema do post?"

    # STEP 4 — TEMA (AGORA USA IA)
    if session["step"] == "tema":

        session["tema"] = message
        session["step"] = "ideias"

        ideias = gerar_ideias_post(
            session["tema"],
            session["plataforma"],
            session["objetivo"]
        )

        return f"""
Aqui vão 3 ideias de post:

{ideias}

Qual você escolhe? (1, 2 ou 3)
"""

    # STEP 5 — ESCOLHA DA IDEIA
    if session["step"] == "ideias":
        session["ideia"] = message
        session["step"] = "estilo"

        return """Qual estilo visual você prefere?

1️⃣ Realismo
2️⃣ Futurista
3️⃣ Surreal
4️⃣ Distopia
"""

    # STEP 6 — ESTILO VISUAL
    if session["step"] == "estilo":
        session["estilo_post"] = message
        session["step"] = "descricao"

        return f"""
Descreva a imagem que você imagina para esse post sobre:

{session["tema"]}

Exemplo:
Pessoa sorrindo em frente a um restaurante em dia de chuva
"""

    # STEP 7 — DESCRIÇÃO DA IMAGEM
    if session["step"] == "descricao":
        session["descricao_post"] = message
        session["step"] = "confirmacao"

        return f"""
Descrição da imagem:

{message}

Está bom ou deseja ajustar?

Digite:
SIM
ou
AJUSTAR
"""

    # STEP 8 — CONFIRMAÇÃO
    if session["step"] == "confirmacao":

        if message.lower() == "sim":

            resultado = gerador_imagem(
                session["estilo_post"],
                session["descricao_post"]
            )

            session["step"] = "final"

            return f"""
🎨 Imagem gerada com sucesso!

Estilo: {resultado["estilo"]}

Descrição:
{resultado["descricao"]}

Seu post está pronto 🚀
"""

        else:
            session["step"] = "descricao"
            return "Ok! Envie a nova descrição da imagem."

    # STEP FINAL
    return "Se quiser criar outro post, diga 'novo post'."
