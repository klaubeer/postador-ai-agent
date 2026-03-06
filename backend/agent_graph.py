from langgraph.graph import StateGraph, END
from backend.state import AgentState

from backend.nodes import (
    generate_idea,
    generate_caption,
    generate_image_prompt,
    generate_hashtags,
    format_post
)

builder = StateGraph(AgentState)

builder.add_node("idea", generate_idea)
builder.add_node("caption", generate_caption)
builder.add_node("image_prompt", generate_image_prompt)
builder.add_node("hashtags", generate_hashtags)
builder.add_node("format", format_post)

builder.set_entry_point("idea")

builder.add_edge("idea", "caption")
builder.add_edge("caption", "image_prompt")
builder.add_edge("image_prompt", "hashtags")
builder.add_edge("hashtags", "format")
builder.add_edge("format", END)

graph = builder.compile()
