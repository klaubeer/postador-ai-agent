from openai import OpenAI

client = OpenAI()


def generate_image(prompt: str) -> dict:
    """
    Gera uma imagem usando OpenAI.
    Retorna:
    {
        "image": base64
    }
    ou
    {
        "error": "mensagem"
    }
    """

    print("IMAGE GEN PROMPT:", prompt)

    try:

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json

        print("IMAGE GENERATED SUCCESSFULLY")

        return {
            "image": image_base64
        }

    except Exception as e:

        error_text = str(e)

        print("IMAGE GENERATION ERROR:", error_text)

        # erro de moderação
        if "moderation_blocked" in error_text or "safety" in error_text:

            return {
                "error": "⚠️ A imagem não pôde ser gerada porque o conteúdo viola as políticas de segurança."
            }

        # erro genérico
        return {
            "error": "⚠️ Ocorreu um erro ao gerar a imagem. Tente novamente."
        }
