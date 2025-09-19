from typing import Any#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict #, Annotated
from langgraph.graph import StateGraph
from agents.world_builder import world_builder_agent
from agents.character_developer import character_dev_agent
from agents.plot_architect import plot_architect_agent
from agents.editor_critic import editor_critic_agent
import langsmith_link

# ---- Define State and Context ---- 
# -------------------------
class AgentState(TypedDict):
    messages: list[dict[str, Any]]
    context: dict[str, Any] | None
    world_outputs: list[dict[str, Any]]
    character_outputs: list[dict[str, Any]]
    plot_outputs: list[dict[str, Any]]
    editor_feedback: list[dict[str, Any]]
    

class Context(TypedDict):
    story_idea: str


# ---- LangGraph Workflow ----
# -------------------------
def world_builder_node(state: AgentState):
    state["world_outputs"]=world_builder_agent(state["context"])
    return state
def character_dev_node(state: AgentState):
    state["character_outputs"]=character_dev_agent(state["context"], state["world_outputs"])
    return state
def plot_architect_node(state: AgentState):
    state["plot_outputs"]=plot_architect_agent(state["context"], state["world_outputs"], state["character_outputs"])
    return state
def editor_critic_node(state: AgentState):
    state["editor_feedback"]=editor_critic_agent(state["context"], state["world_outputs"], state["character_outputs"], state["plot_outputs"])
    return state

workflow = StateGraph(state_schema=AgentState, context_schema=Context)

workflow.add_node("World Builder", world_builder_node)
workflow.add_node("Character Developer", character_dev_node)
workflow.add_node("Plot Architect", plot_architect_node)
workflow.add_node("Editor/Critic", editor_critic_node)

workflow.set_entry_point("World Builder")
workflow.add_edge("World Builder", "Character Developer")
workflow.add_edge("Character Developer", "Plot Architect")
workflow.add_edge("Plot Architect", "Editor/Critic")
workflow.add_edge( "Editor/Critic", END)

app = workflow.compile()

# story_idea = "A young explorer discovers a hidden magical kingdom in the mountains."

# initial_state = {"context": story_idea}

# result = app.invoke(initial_state)

# print(result)

# ---- Run Session ----
# -------------------------
if __name__ == "__main__":
    # prompt = "Develop a dark fantasy world about a city floating above a poisonous sea."
    prompt = "Develop a post-apocalyptic world with dark, ethically challenging situations."
    # result = app.invoke({"messages": [{"role": "user", "content": prompt}]})
    initial_state = {"context": prompt}
    result = app.invoke(initial_state)
    print("\nFINAL CREATIVE PACKAGE:\n")
    # print(result["messages"][-1]["content"])
    print(result["editor_feedback"]) #[-1]["content"]
