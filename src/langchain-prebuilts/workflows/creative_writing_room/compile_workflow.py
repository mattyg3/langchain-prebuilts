from typing import Any, TypedDict#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
# from typing_extensions import TypedDict #, Annotated
from langgraph.graph import StateGraph
from .agents.world_builder import world_builder_agent
from .agents.character_developer import character_dev_agent
from .agents.plot_architect import plot_architect_agent
from .agents.editor_critic import editor_critic_agent
from .agents.head_writer import head_writer_agent
# from agents.world_builder import world_builder_agent
# from agents.character_developer import character_dev_agent
# from agents.plot_architect import plot_architect_agent
# from agents.editor_critic import editor_critic_agent
# from agents.head_writer import head_writer_agent
# import langsmith_link
# ---- Define State and Context ---- 
# -------------------------
class AgentState(TypedDict):
    messages: list[dict[str, Any]]
    context: dict[str, Any] | None
    world_outputs: list[dict[str, Any]]
    character_outputs: list[dict[str, Any]]
    plot_outputs: list[dict[str, Any]]
    editor_feedback: list[dict[str, Any]]
    head_writer_outputs: list[dict[str, Any]]

def create_agent_state(messages=[], context=None, world_outputs=[], character_outputs=[], plot_outputs=[], editor_feedback=[], head_writer_outputs=[]) -> AgentState:
    return AgentState(
        messages=messages,
        context=context,
        world_outputs=world_outputs,
        character_outputs=character_outputs,
        plot_outputs=plot_outputs,
        editor_feedback=editor_feedback,
        head_writer_outputs=head_writer_outputs
    )
    
# class Context(TypedDict):
#     story_idea: str


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
def head_writer_node(state: AgentState):
    state["head_writer_outputs"]=head_writer_agent(state["context"], state["world_outputs"], state["character_outputs"], state["plot_outputs"], state["editor_feedback"])
    return state

workflow = StateGraph(state_schema=AgentState) #, context_schema=Context

workflow.add_node("World Builder", world_builder_node)
workflow.add_node("Character Developer", character_dev_node)
workflow.add_node("Plot Architect", plot_architect_node)
workflow.add_node("Editor/Critic", editor_critic_node)
workflow.add_node("Head Writer", head_writer_node)

workflow.set_entry_point("World Builder")
workflow.add_edge("World Builder", "Character Developer")
workflow.add_edge("Character Developer", "Plot Architect")
workflow.add_edge("Plot Architect", "Editor/Critic")
workflow.add_edge("Editor/Critic", "Head Writer")
# workflow.add_edge( "Editor/Critic", END)

app = workflow.compile()


# ---- Helper: dependency-aware selective runner ----
def run_selected_agents(state: AgentState, requested: list[str]) -> AgentState:
    """
    requested: subset of ['w','c','p','e']
    Runs agents in dependency order and auto-runs any upstream agents
    if their outputs are missing.
    """
    # Track which outputs are already present
    have_world = bool(state["world_outputs"])
    have_char = bool(state["character_outputs"])
    have_plot = bool(state["plot_outputs"])

    # Expand requested list to include missing dependencies
    expanded = set(requested)
    if "c" in requested and not have_world:
        expanded.add("w")
    if "p" in requested:
        if not have_world:
            expanded.add("w")
        if not have_char:
            expanded.add("c")
    if "e" in requested:
        if not have_world:
            expanded.add("w")
        if not have_char:
            expanded.add("c")
        if not have_plot:
            expanded.add("p")

    # Order of execution respecting dependencies
    order = [a for a in ["w", "c", "p", "e"] if a in expanded]

    for agent in order:
        if agent == "w":
            state = world_builder_node(state)
        elif agent == "c":
            state = character_dev_node(state)
        elif agent == "p":
            state = plot_architect_node(state)
        elif agent == "e":
            state = editor_critic_node(state)
    return state

