from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):

    session_id: str
    message: str

    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]

    intent: Optional[str]

    resposta: str
