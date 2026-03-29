from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.nodes import generate_content, generate_image_prompt

builder = StateGraph(AgentState)

builder.add_node("content", generate_content)
builder.add_node("image_prompt", generate_image_prompt)

builder.set_entry_point("content")

builder.add_edge("content", "image_prompt")
builder.add_edge("image_prompt", END)

graph = builder.compile()
