def generate_image_prompt(state):

    idea = state.get("melhor_ideia")
    legenda = state.get("legenda")

    prompt = f"""
social media marketing photo, {idea},
context: {legenda},
professional photography, modern lighting,
clean composition, high engagement social media style
"""

    state["image_prompt"] = prompt.strip()
    state["awaiting_image_approval"] = True

    return state
