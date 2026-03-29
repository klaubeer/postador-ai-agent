import httpx
from urllib.parse import quote


def generate_image(prompt: str) -> dict:
    """Gera imagem via Pollinations.ai (grátis, sem API key)."""

    print(f"[IMAGE] prompt: {prompt}")

    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"

    try:
        # pollinations retorna a imagem diretamente
        # retornamos a URL para o frontend exibir (sem base64)
        # fazemos um HEAD request pra verificar se a URL funciona
        response = httpx.head(url, follow_redirects=True, timeout=60.0)

        if response.status_code == 200:
            print("[IMAGE] URL gerada com sucesso")
            return {"image_url": url}

        print(f"[IMAGE] erro: status {response.status_code}")
        return {"error": "Erro ao gerar imagem. Tente novamente."}

    except httpx.TimeoutException:
        # pollinations pode demorar na primeira geração
        # mas a URL ainda funciona — retorna mesmo assim
        print("[IMAGE] timeout no HEAD, retornando URL mesmo assim")
        return {"image_url": url}

    except Exception as e:
        print(f"[IMAGE] erro: {e}")
        return {"error": "Erro ao gerar imagem. Tente novamente."}
