from typing import TypedDict, Optional, List, Dict


class AgentState(TypedDict, total=False):

    session_id: str
    message: str

    history: List[Dict]

    intent: Optional[str]

    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]

    resposta: str
