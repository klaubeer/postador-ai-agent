from urllib.parse import quote


def generate_image(prompt: str) -> dict:
    """Gera URL de imagem via Pollinations.ai (grátis, sem API key).

    A URL do Pollinations é determinística — a imagem é gerada
    no primeiro acesso. Não fazemos request nenhum aqui, apenas
    montamos a URL e deixamos o browser do usuário carregar.
    """

    if not prompt:
        return {"error": "Prompt de imagem vazio."}

    print(f"[IMAGE] prompt: {prompt}")

    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"

    print(f"[IMAGE] URL: {url}")

    return {"image_url": url}
