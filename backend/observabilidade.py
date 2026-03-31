"""Inicialização do Sentinela — observabilidade LLM para o Postador."""

import os
from dotenv import load_dotenv
from sentinela import Sentinela
from sentinela.decoradores import _obter_cliente

load_dotenv()

PROJETO = "postador"

sentinela = Sentinela(
    api_key=os.getenv("SENTINELA_API_KEY", ""),
    projeto=PROJETO,
    base_url=os.getenv("SENTINELA_URL", "http://localhost:8000"),
)


def get_cliente():
    return _obter_cliente()
