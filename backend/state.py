from typing import TypedDict, List


class AgentState(TypedDict):

    user_input: str

    objetivo: str
    publico: str
    plataforma: str
    tema: str

    ideias: List[str]
    melhor_ideia: str

    legenda: str
    image_prompt: str
    hashtags: List[str]

    post_final: str
