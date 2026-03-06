from openai import OpenAI

client = OpenAI()


def generate_image(prompt: str) -> str:
    """
    Gera uma imagem usando OpenAI e retorna o base64 da imagem.
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

        return image_base64

    except Exception as e:
        print("IMAGE GENERATION ERROR:", e)
        return None
