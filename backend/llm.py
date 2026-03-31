import asyncio
import time
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv
from sentinela.modelos import Trace

load_dotenv()

client = OpenAI()

MODEL = "gpt-4.1-mini"

# Preços gpt-4.1-mini (USD por token)
_CUSTO_INPUT = 0.40 / 1_000_000
_CUSTO_OUTPUT = 1.60 / 1_000_000


def _enviar_trace(nome: str, input_data, output_data, tokens_in: int, tokens_out: int, latencia_ms: float):
    from backend.observabilidade import get_cliente, PROJETO
    cliente = get_cliente()
    if not cliente:
        return
    trace = Trace(
        projeto=PROJETO,
        nome=nome,
        input=input_data,
        output=output_data,
        modelo=MODEL,
        tokens_entrada=tokens_in,
        tokens_saida=tokens_out,
        latencia_ms=round(latencia_ms, 2),
        custo_usd=round(tokens_in * _CUSTO_INPUT + tokens_out * _CUSTO_OUTPUT, 8),
        criado_em=datetime.utcnow(),
    )
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(cliente.enviar_trace(trace))
    except RuntimeError:
        asyncio.run(cliente.enviar_trace(trace))

# token tracking por sessão
_session_tokens: dict[str, int] = {}
MAX_SESSION_TOKENS = 10000


def reset_session(session_id: str):
    _session_tokens.pop(session_id, None)


def llm(prompt: str, system: str = None, session_id: str = None, json_mode: bool = False, nome: str = "llm") -> str:

    # verifica limite
    if session_id and _session_tokens.get(session_id, 0) >= MAX_SESSION_TOKENS:
        return "Limite de tokens atingido para esta sessão."

    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": MODEL,
        "messages": messages,
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    inicio = time.perf_counter()
    response = client.chat.completions.create(**kwargs)
    latencia_ms = (time.perf_counter() - inicio) * 1000

    text = response.choices[0].message.content
    usage = response.usage

    if session_id:
        _session_tokens[session_id] = _session_tokens.get(session_id, 0) + usage.total_tokens

    print(f"[LLM] tokens: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens}"
          + (f" | session {session_id}: {_session_tokens.get(session_id, 0)}" if session_id else ""))

    _enviar_trace(nome, prompt, text, usage.prompt_tokens, usage.completion_tokens, latencia_ms)

    return text


def llm_chat(messages: list, system: str = None, session_id: str = None, json_mode: bool = False, nome: str = "llm-chat") -> str:

    if session_id and _session_tokens.get(session_id, 0) >= MAX_SESSION_TOKENS:
        return "Limite de tokens atingido para esta sessão."

    full_messages = []

    if system:
        full_messages.append({"role": "system", "content": system})

    full_messages.extend(messages)

    kwargs = {
        "model": MODEL,
        "messages": full_messages,
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    inicio = time.perf_counter()
    response = client.chat.completions.create(**kwargs)
    latencia_ms = (time.perf_counter() - inicio) * 1000

    text = response.choices[0].message.content
    usage = response.usage

    if session_id:
        _session_tokens[session_id] = _session_tokens.get(session_id, 0) + usage.total_tokens

    print(f"[LLM] tokens: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens}"
          + (f" | session {session_id}: {_session_tokens.get(session_id, 0)}" if session_id else ""))

    _enviar_trace(nome, messages, text, usage.prompt_tokens, usage.completion_tokens, latencia_ms)

    return text
