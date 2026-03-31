"""Inicialização do Sentinela — observabilidade LLM para o Postador."""

import os
from dotenv import load_dotenv
from sentinela import Sentinela

load_dotenv()

sentinela = Sentinela(
    api_key=os.getenv("SENTINELA_API_KEY", ""),
    projeto="postador",
    base_url=os.getenv("SENTINELA_URL", "http://localhost:8000"),
)
