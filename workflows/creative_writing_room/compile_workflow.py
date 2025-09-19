from typing import Any#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict #, Annotated
from langgraph.graph import StateGraph
from agents.world_builder import world_builder_agent
from agents.character_developer import character_dev_agent
from agents.plot_architect import plot_architect_agent
from agents.editor_critic import editor_critic_agent
from agents.head_writer import head_writer_agent
import langsmith_link
# from utils.output_formatting import format_feedback
from output_formatting import format_feedback
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
def head_writer_node(state: AgentState):
    state["head_writer_outputs"]=head_writer_agent(state["context"], state["world_outputs"], state["character_outputs"], state["plot_outputs"], state["editor_feedback"])
    return state

workflow = StateGraph(state_schema=AgentState, context_schema=Context)

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

# story_idea = "A young explorer discovers a hidden magical kingdom in the mountains."

# initial_state = {"context": story_idea}

# result = app.invoke(initial_state)

# print(result)

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

# ---- Run Session ----
# -------------------------
# if __name__ == "__main__":
#     # prompt = "Develop a dark fantasy world about a city floating above a poisonous sea."
#     prompt = "Develop a post-apocalyptic world with dark, ethically challenging situations."
#     # result = app.invoke({"messages": [{"role": "user", "content": prompt}]})
#     initial_state = {"context": prompt}
#     result = app.invoke(initial_state)
#     print("\nFINAL CREATIVE PACKAGE:\n")
#     # print(result["messages"][-1]["content"])
#     print(result["editor_feedback"]) #[-1]["content"]

# ---- Interactive Session ----
if __name__ == "__main__":
    prompt = "Develop a story about an Atlantis type civilization. An early plot point should be a catastrophic event, resulting in our characters needing to learn how to survive without their advanced technology."

    state: AgentState = {
        "messages": [{"role": "user", "content": prompt}],
        "context": {"story_idea": prompt},
        "world_outputs": [],
        "character_outputs": [],
        "plot_outputs": [],
        "editor_feedback": [],
        "head_writer_outputs": [],
    }

    # Initial full pipeline run
    state = app.invoke(state)
    print("\nFINAL CREATIVE PACKAGE:\n")
    for chunk in state["head_writer_outputs"]:
        print(format_feedback(chunk))

    while True:
        follow = input("\n[Follow-up] Enter more questions/ideas (or 'exit'): ").strip()
        if follow.lower() in {"exit", "quit", "done", "finished"}:
            print("Session ended.")
            break

        state["messages"].append({"role": "user", "content": follow})
        state["context"]["story_idea"] = follow  # optional: treat as new seed

        choice = input(
            "Which agents to rerun? "
            "[a]ll, [w]orld, [c]haracter, [p]lot, [e]ditor (e.g. wc): "
        ).strip().lower()

        if choice in {"a", ""}:
            # Empty or 'a' => full run
            state = app.invoke(state)
        else:
            # Dependency-aware partial run
            state = run_selected_agents(state, list(choice))

        print("\nUPDATED CREATIVE PACKAGE:\n")
        for chunk in state["head_writer_outputs"]:
            print(format_feedback(chunk))
