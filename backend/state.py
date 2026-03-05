from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):

    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]
    publico: Optional[str]

    ideias: Optional[str]
    melhor_ideia: Optional[str]
    legenda: Optional[str]
    image_prompt: Optional[str]
    hashtags: Optional[str]
    post_final: Optional[str]
