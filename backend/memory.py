# backend/memory.py

sessions = {}

def get_session(session_id):

    if session_id not in sessions:
        sessions[session_id] = {
            "step": "inicio",
            "objetivo": None,
            "plataforma": None,
            "tema": None,
            "ideia": None,
            "estilo_post": None,
            "descricao_post": None
        }

    return sessions[session_id]
