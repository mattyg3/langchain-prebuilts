from typing import Any, TypedDict#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
from langgraph.graph import StateGraph
from .agents.greeter_interview import greeting_agent
from .agents.world_builder import world_builder_agent
from .agents.character_developer import character_dev_agent
from .agents.plot_architect import plot_architect_agent
# from .agents.editor_critic import editor_critic_agent
from .agents.head_writer import head_writer_agent
from util_funcs import format_feedback, save_graph_state, get_persona
from langchain_core.runnables import RunnableLambda

# ---- Define State ---- 
# -------------------------
class AgentState(TypedDict):
    #core outputs#
    context:  str | None #dict[str, Any]
    messages: list[dict[str, Any]]
    #agent outputs#
    world_outputs: list[dict[str, Any]]
    character_outputs: list[dict[str, Any]]
    plot_outputs: list[dict[str, Any]]
    head_writer_outputs: list[dict[str, Any]]
    #graph helpers#
    routing: str
    routing_list: list[str]
    # editor_feedback: list[dict[str, Any]]
    # need_human_bool: bool
    # human_answer: list[dict[str, Any]]
    # follow_up: list[dict[str, Any]]
    
def create_agent_state(
        #core outputs#
        context=None, 
        messages=[], 
        #agent outputs#
        world_outputs=[], 
        character_outputs=[], 
        plot_outputs=[], 
        head_writer_outputs=[], 
        #graph helpers#
        routing=None, 
        routing_list=[]) -> AgentState:
    return AgentState(
        #core outputs#
        context=context,
        messages=messages,
        #agent outputs#
        world_outputs=world_outputs,
        character_outputs=character_outputs,
        plot_outputs=plot_outputs,
        head_writer_outputs=head_writer_outputs,
        #graph helpers#
        routing=routing,
        routing_list=routing_list,


        # editor_feedback=editor_feedback,
        # need_human_bool=need_human_bool,
        # human_answer=human_answer,
        # follow_up=follow_up,
        
    )


# ---- LangGraph Workflow ----
workflow = StateGraph(state_schema=AgentState) #, context_schema=Context
# -------------------------

### --- Nodes ---
def human_node(state: AgentState):
    answer = input(f"\nApprove of story outline? (yes/no) \n").lower()
    if 'yes' in answer or 'y' in answer:
        state['routing'] = "yes"
    elif 'no' in answer or 'n' in answer:
        state['routing'] = "no"
    else:
        state['routing'] = "yes" 
    return state 
workflow.add_node("Human Node", RunnableLambda(human_node))

def follow_up_node(state: AgentState):
    answer = input(f"\nWhich component(s) need reworking? ['world', 'plot', 'characters', 'all'] \n").lower()
    state['routing_list'] = []
    
    if 'world' in answer:
        state['routing_list'].append('world')
    if 'plot' in answer:
        state['routing_list'].append('plot')
    if 'characters' in answer:
        state['routing_list'].append('characters')
    
    details = input(f"\nProvide any additional details or guidelines for changes you want to see.\n").lower()

    state['context'] = state['context'] + [f'\nUser was not satisfied with the provided story, make improvements to your story component. User provided guidelines: {details}\n']

    return state
workflow.add_node("Follow Up", RunnableLambda(follow_up_node))

def greeter_node(state: AgentState):
    greeting = f"\nHey!, \nI'm an expert story crafter that has a team of specialized agents at my disposal. \nGive me some details about the story you want.\n\n\nInput:\n"
    answer = input(greeting).lower()
    response = greeting_agent(answer)
    state["context"] = response
    state["messages"].append({"role": "greeter", "content": greeting})
    state["messages"].append({"role": "user", "content": answer})
    state["messages"].append({"role": "greeter", "content": response})
    state["routing_list"] = ['world', 'plot', 'characters'] #init run should go through all nodes
    return state
workflow.add_node("Greeting Node", greeter_node)

def world_builder_node(state: AgentState):
    print('\n\nGenerating..') #currently go through all agent nodes
    if 'world' in state["routing_list"]:
        print('     Building the World..')
        response = world_builder_agent(state["context"], persona=get_persona(persona='Worldbuilder'))
        state["world_outputs"].append(response)
        state["messages"].append({"role": "world_builder", "content": response})
    return state
workflow.add_node("World Builder", world_builder_node)

def character_dev_node(state: AgentState):
    if 'characters' in state["routing_list"]:
        print('     Developing Characters..')
        response = character_dev_agent(state["context"], persona=get_persona(persona='Archetype')) # only last output from world_builder , state["world_outputs"][-1]
        state["character_outputs"].append(response)
        state["messages"].append({"role": "character_developer", "content": response})
    return state
workflow.add_node("Character Developer", character_dev_node)

def plot_architect_node(state: AgentState):
    if 'plot' in state["routing_list"]:
        print('     Creating Plot & Story Arcs..')
        response = plot_architect_agent(state["context"], persona=get_persona(persona='Pacer')) # only last output , state["world_outputs"][-1], state["character_outputs"][-1]
        state["plot_outputs"].append(response)
        state["messages"].append({"role": "plot_architect", "content": response})
    return state
workflow.add_node("Plot Architect", plot_architect_node)

# def editor_critic_node(state: AgentState):
#     print('Critiquing..')
#     response = editor_critic_agent(state["context"], state["world_outputs"][-1], state["character_outputs"][-1], state["plot_outputs"][-1]) # only last output
#     state["editor_feedback"].append(response)
#     state["messages"].append({"role": "editor_critic", "content": response})
#     return state
# workflow.add_node("Editor/Critic", editor_critic_node)

def head_writer_node(state: AgentState):
    print('     Summarizing..')
    response = head_writer_agent(state["context"], state["world_outputs"][-1], state["character_outputs"][-1], state["plot_outputs"][-1], persona=get_persona(persona='Narrator')) # only last output , state["editor_feedback"][-1] 
    state["head_writer_outputs"].append(response)
    state["messages"].append({"role": "head_writer", "content": response})
    print("\n\n------------ Head Writer ------------\n")
    for msg in state["messages"][-1]["content"]:
        print(format_feedback(msg))
    return state
workflow.add_node("Head Writer", head_writer_node)

def save_node(state: AgentState):
    save_graph_state(state, file_name='save_state')
    return state
workflow.add_node("Save Node", RunnableLambda(save_node))

### --- Edges ---
workflow.set_entry_point("Greeting Node")
workflow.add_edge("Greeting Node", "World Builder")
workflow.add_edge("World Builder", "Character Developer")
workflow.add_edge("Character Developer", "Plot Architect")
workflow.add_edge("Plot Architect", "Head Writer")
# workflow.add_edge("Plot Architect", "Editor/Critic")
# workflow.add_edge("Editor/Critic", "Head Writer")
workflow.add_edge("Head Writer", "Human Node")
workflow.add_conditional_edges(
    "Human Node", # source node
    lambda s: s.get("routing", "yes"),
    {"yes": "Save Node", "no": "Follow Up"}
)
workflow.add_edge("Save Node", END)
workflow.add_edge("Follow Up", "World Builder")

app = workflow.compile()

