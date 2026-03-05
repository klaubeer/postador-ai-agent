from openai import OpenAI

client = OpenAI()

def generate_image(prompt):

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    return result.data[0].url
