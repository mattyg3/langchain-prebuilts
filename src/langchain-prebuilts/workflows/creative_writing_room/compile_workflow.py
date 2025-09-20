from typing import Any, TypedDict#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
from langgraph.graph import StateGraph
from .agents.greeter_interview import greeting_agent
from .agents.world_builder import world_builder_agent
from .agents.character_developer import character_dev_agent
from .agents.plot_architect import plot_architect_agent
from .agents.editor_critic import editor_critic_agent
from .agents.head_writer import head_writer_agent
from util_funcs import format_feedback
from langchain_core.runnables import RunnableLambda

# ---- Define State and Context ---- 
# -------------------------
class AgentState(TypedDict):
    context: dict[str, Any] | None
    messages: list[dict[str, Any]]
    world_outputs: list[dict[str, Any]]
    character_outputs: list[dict[str, Any]]
    plot_outputs: list[dict[str, Any]]
    editor_feedback: list[dict[str, Any]]
    head_writer_outputs: list[dict[str, Any]]
    need_human_bool: bool
    human_answer: list[dict[str, Any]]
    follow_up: list[dict[str, Any]]

def create_agent_state(context=None, messages=[], world_outputs=[], character_outputs=[], plot_outputs=[], editor_feedback=[], head_writer_outputs=[], need_human_bool=False, human_answer=[], follow_up=[]) -> AgentState:
    return AgentState(
        context=context,
        messages=messages,
        world_outputs=world_outputs,
        character_outputs=character_outputs,
        plot_outputs=plot_outputs,
        editor_feedback=editor_feedback,
        head_writer_outputs=head_writer_outputs,
        need_human_bool=need_human_bool,
        human_answer=human_answer,
        follow_up=follow_up
    )


# ---- LangGraph Workflow ----
# -------------------------
def human_node(state: AgentState):
    # Track which outputs are already present
    # have_world = bool(state["world_outputs"])
    # have_char = bool(state["character_outputs"])
    # have_plot = bool(state["plot_outputs"])
    # have_feedback = bool(state["editor_feedback"])
    # have_head_writer = bool(state["head_writer_outputs"])
    # if have_head_writer:
    #     answer = input(f"Approve of story outline? (yes/no) ").lower()
    #     state["human_answer"].append(answer)
    #     state["context"]=answer
        # return {"human_answer": answer}
    # else:
    #     # answer = input("Provide input: ").lower()
    #     # state["human_answer"].append(answer)
    #     # state["context"]=answer
    #     # return {"human_answer": answer}
    #     pass
    answer = input(f"Approve of story outline? (yes/no) ").lower()
    if 'yes' in answer:
        return "yes"
    elif 'no' in answer:
        return "no"
    else:
        return "yes"

def greeter_node(state: AgentState):
    greeting = f"\nHey!, \nI'm an expert story crafter that has a team of specialized agents at my disposal. \nGive me some details about the story you want.\n\n\n\n\n\nInput:\n"
    answer = input(greeting).lower()
    response = greeting_agent(answer)
    state["context"] = response
    state["messages"].append({"role": "greeter", "content": greeting})
    state["messages"].append({"role": "user", "content": answer})
    state["messages"].append({"role": "greeter", "content": response})
    return state
def world_builder_node(state: AgentState):
    print('Building the World..')
    response = world_builder_agent(state["context"])
    state["world_outputs"].append(response)
    state["messages"].append({"role": "world_builder", "content": response})
    return state
def character_dev_node(state: AgentState):
    print('Developing Characters..')
    response = character_dev_agent(state["context"], state["world_outputs"][-1]) # only last output from world_builder
    state["character_outputs"].append(response)
    state["messages"].append({"role": "character_developer", "content": response})
    return state
def plot_architect_node(state: AgentState):
    print('Creating Plot & Story Arcs..')
    response = plot_architect_agent(state["context"], state["world_outputs"][-1], state["character_outputs"][-1]) # only last output
    state["plot_outputs"].append(response)
    state["messages"].append({"role": "plot_architect", "content": response})
    return state
def editor_critic_node(state: AgentState):
    print('Critiquing..')
    response = editor_critic_agent(state["context"], state["world_outputs"][-1], state["character_outputs"][-1], state["plot_outputs"][-1]) # only last output
    state["editor_feedback"].append(response)
    state["messages"].append({"role": "editor_critic", "content": response})
    return state
def head_writer_node(state: AgentState):
    print('Summarizing..')
    response = head_writer_agent(state["context"], state["world_outputs"][-1], state["character_outputs"][-1], state["plot_outputs"][-1], state["editor_feedback"][-1]) # only last output
    state["head_writer_outputs"].append(response)
    state["messages"].append({"role": "head_writer", "content": response})
    state["need_human_bool"] = False
    #Display
    for msg in state["messages"][-1]["content"]:
        print(format_feedback(msg))
    return state
# def follow_up_node(state: AgentState):
#     components = ['world', 'plot', 'characters']
#     answer = input(f"What portion needs to be improved? ({components})").lower()
#     if all(s in answer for s in components):
#         # state["need_human_bool"] = True
#         pass
#     elif not any(s in answer for s in components):
#         pass
#     else:
#         s_list=[]
#         for s in components:
#             if s in answer:
#                 s_list.append(a)
#         state["follow_up"]=({"routing": s})
        
        
        


#     state["human_answer"].append(answer)
#     state["context"] = f"Initial input: {state['context']}. \n\nOutline Provided: {state['head_writer_outputs'][-1]}. \n\nUser Feedback: {state['human_answer'][-1]}"
#     return state

workflow = StateGraph(state_schema=AgentState) #, context_schema=Context

workflow.add_node("Human Node", RunnableLambda(human_node))
# workflow.add_node("Follow Up", follow_up_node)

workflow.add_node("Greeting Node", greeter_node)
workflow.add_node("World Builder", world_builder_node)
workflow.add_node("Character Developer", character_dev_node)
workflow.add_node("Plot Architect", plot_architect_node)
workflow.add_node("Editor/Critic", editor_critic_node)
workflow.add_node("Head Writer", head_writer_node)

workflow.set_entry_point("Greeting Node")
# workflow.add_edge("Greeting Node", "Human Node")
# # workflow.set_entry_point("Human Node")
# workflow.add_edge("Human Node", "World Builder")
workflow.add_edge("Greeting Node", "World Builder")
 
workflow.add_edge("World Builder", "Character Developer")
workflow.add_edge("Character Developer", "Plot Architect")
workflow.add_edge("Plot Architect", "Editor/Critic")
workflow.add_edge("Editor/Critic", "Head Writer")
workflow.add_edge("Head Writer", "Human Node")
workflow.add_conditional_edges(
    "Human Node", # source node
    human_node,
    {"yes": END, "no": "Greeting Node"}
)
# workflow.add_conditional_edges(
#     "Follow Up", # source node
#     follow_up_node,
#     {"world": "", 
#      "plot": "",
#      "characters": "",
#      }
# )
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

