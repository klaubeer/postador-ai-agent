def generate_image_prompt(state):

    idea = state.get("melhor_ideia")
    legenda = state.get("legenda")

    prompt = f"""
marketing photo for social media

concept: {idea}

caption context:
{legenda}

style:
modern marketing photography
clean lighting
professional product shot
high engagement social media style
"""

    state["image_prompt"] = prompt
    state["awaiting_image_approval"] = True

    return state
