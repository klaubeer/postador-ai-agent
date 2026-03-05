from typing import TypedDict, List, Dict, Optional

class AgentState(TypedDict, total=False):

    session_id: str
    message: str

    history: List[Dict]

    resposta: str

    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]
