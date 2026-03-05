from typing import TypedDict, Optional

class AgentState(TypedDict):

    message: str

    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]

    ideias: Optional[str]
    resposta: Optional[str]
