from langgraph.graph import StateGraph, END
from backend.state import AgentState

from backend.nodes import (
    generate_ideas,
    select_best_idea,
    generate_caption,
    generate_image_prompt,
    generate_hashtags,
    format_post
)

builder = StateGraph(AgentState)

builder.add_node("ideas", generate_ideas)
builder.add_node("select", select_best_idea)
builder.add_node("caption", generate_caption)
builder.add_node("image_prompt", generate_image_prompt)
builder.add_node("hashtags", generate_hashtags)
builder.add_node("format", format_post)

builder.set_entry_point("ideas")

builder.add_edge("ideas", "select")
builder.add_edge("select", "caption")
builder.add_edge("caption", "image_prompt")
builder.add_edge("image_prompt", "hashtags")
builder.add_edge("hashtags", "format")
builder.add_edge("format", END)

graph = builder.compile()
