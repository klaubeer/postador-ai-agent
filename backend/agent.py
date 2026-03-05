from memory import get_session

def agent_chat(session_id, message):

    session = get_session(session_id)

    if session["step"] == "inicio":
        session["step"] = "objetivo"

        return "Qual é o objetivo desse post?\nVender\nEngajar\nEducar\nInspirar\nEntreter"

    if session["step"] == "objetivo":
        session["objetivo"] = message
        session["step"] = "plataforma"

        return "Em qual plataforma será publicado?"

    if session["step"] == "plataforma":
        session["plataforma"] = message
        session["step"] = "tema"

        return "Qual é o tema do post?"

    if session["step"] == "tema":
        session["tema"] = message
        session["step"] = "ideias"

        return f"""
Aqui vão 3 ideias para {message}:

1️⃣ Dica prática
2️⃣ Curiosidade
3️⃣ História inspiradora

Qual você escolhe?
"""
