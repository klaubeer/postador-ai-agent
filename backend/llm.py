from openai import OpenAI

client = OpenAI()

MAX_SESSION_TOKENS = 8000
session_tokens = 0


def llm(prompt):

    global session_tokens

    # bloqueia se estourar limite
    if session_tokens >= MAX_SESSION_TOKENS:
        return "⚠️ Token limit reached for this session."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response.choices[0].message.content
    usage = response.usage

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    session_tokens += total_tokens

    print("\n====== TOKEN USAGE ======")
    print("prompt:", prompt_tokens)
    print("completion:", completion_tokens)
    print("total:", total_tokens)
    print("session total:", session_tokens)
    print("=========================\n")

    return text
