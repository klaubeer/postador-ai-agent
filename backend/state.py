from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):

    # contexto coletado pelo planner
    objetivo: Optional[str]
    plataforma: Optional[str]
    tema: Optional[str]
    publico: Optional[str]
    detalhes: Optional[str]

    # stage do fluxo
    stage: Optional[str]  # collecting, choosing_idea, choosing_style, confirming_image, done

    # gerados pelo pipeline
    ideias_raw: Optional[str]
    ideia_escolhida: Optional[str]
    estilo_visual: Optional[str]
    legenda: Optional[str]
    hashtags: Optional[str]
    descricao_imagem: Optional[str]
    image_prompt: Optional[str]
    image_url: Optional[str]
    post_final: Optional[str]
