from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):

    # contexto coletado pelo planner
    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]
    publico: Optional[str]
    detalhes: Optional[str]

    # gerados pelo pipeline
    ideias: Optional[str]
    melhor_ideia: Optional[str]
    legenda: Optional[str]
    hashtags: Optional[str]
    image_prompt: Optional[str]
    image_url: Optional[str]
    post_final: Optional[str]
