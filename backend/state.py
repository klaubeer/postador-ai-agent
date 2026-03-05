from typing import TypedDict


class AgentState(TypedDict, total=False):

    session_id: str
    message: str
    step: str

    objetivo: str
    plataforma: str
    tema: str

    resposta: str
