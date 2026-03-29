from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

MODEL = "gpt-4.1-mini"

# token tracking por sessão
_session_tokens: dict[str, int] = {}
MAX_SESSION_TOKENS = 10000


def reset_session(session_id: str):
    _session_tokens.pop(session_id, None)


def llm(prompt: str, system: str = None, session_id: str = None, json_mode: bool = False) -> str:

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

    response = client.chat.completions.create(**kwargs)

    text = response.choices[0].message.content
    usage = response.usage

    if session_id:
        _session_tokens[session_id] = _session_tokens.get(session_id, 0) + usage.total_tokens

    print(f"[LLM] tokens: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens}"
          + (f" | session {session_id}: {_session_tokens.get(session_id, 0)}" if session_id else ""))

    return text


def llm_chat(messages: list, system: str = None, session_id: str = None, json_mode: bool = False) -> str:

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

    response = client.chat.completions.create(**kwargs)

    text = response.choices[0].message.content
    usage = response.usage

    if session_id:
        _session_tokens[session_id] = _session_tokens.get(session_id, 0) + usage.total_tokens

    print(f"[LLM] tokens: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens}"
          + (f" | session {session_id}: {_session_tokens.get(session_id, 0)}" if session_id else ""))

    return text
