from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.nodes import generate_ideas, generate_final_post, generate_image_prompt


# --- Graph 1: gerar ideias ---
ideas_builder = StateGraph(AgentState)
ideas_builder.add_node("ideas", generate_ideas)
ideas_builder.set_entry_point("ideas")
ideas_builder.add_edge("ideas", END)
ideas_graph = ideas_builder.compile()


# --- Graph 2: gerar post final + image prompt ---
post_builder = StateGraph(AgentState)
post_builder.add_node("final_post", generate_final_post)
post_builder.add_node("image_prompt", generate_image_prompt)
post_builder.set_entry_point("final_post")
post_builder.add_edge("final_post", "image_prompt")
post_builder.add_edge("image_prompt", END)
post_graph = post_builder.compile()
