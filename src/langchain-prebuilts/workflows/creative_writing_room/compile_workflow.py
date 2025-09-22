from typing import Any, TypedDict#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
from .agents.greeter_interview import greeting_agent
from .agents.world_builder import world_builder_agent
from .agents.character_developer import character_dev_agent
from .agents.plot_architect import plot_architect_agent
# from .agents.editor_critic import editor_critic_agent
from .agents.head_writer import head_writer_agent
from util_funcs import format_feedback, save_graph_state, get_persona #, get_plot
from langchain_core.runnables import RunnableLambda

def print_state_message(state):
    for msg in state["messages"][-1]["content"]:
            print(format_feedback(msg))

# def y_n_process_input(state_elem):

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
    optional_human_nodes: bool
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
        routing="yes", 
        routing_list=[],
        optional_human_nodes=False) -> AgentState:
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
        optional_human_nodes=optional_human_nodes,


        # editor_feedback=editor_feedback,
        # need_human_bool=need_human_bool,
        # human_answer=human_answer,
        # follow_up=follow_up,
        
    )


# ---- LangGraph Workflow ----
workflow = StateGraph(state_schema=AgentState) #, context_schema=Context
# -------------------------

### --- Nodes ---
#### --- Entry ---
def greeter_node(state: AgentState):
    greeting = f"\nHey!, \nI'm an expert story crafter that has a team of specialized agents at my disposal. \nGive me some details about the story you want.\n\n\nInput:\n"
    answer = input(greeting).lower()
    # response = greeting_agent(answer)
     #+ str(response)
    state["messages"].append({"role": "greeter", "content": greeting})
    state["messages"].append({"role": "user", "content": answer})
    # state["messages"].append({"role": "greeter", "content": response})
    state["routing_list"] = ['world', 'plot', 'characters'] #init run should go through all nodes
    state["context"] = state["context"] + f'\nUser: {answer}\n'
    return state
workflow.add_node("Greeting Node", greeter_node)

#### --- Human Inputs ---
def human_node(state: AgentState):
    answer = input(f"\n\nApprove of story outline? (yes/no) \n").lower()
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

    # state['context'] = state['context'] + [f'\nUser was not satisfied with the provided story, make improvements to your story component. User provided guidelines: {details}\n']
    state['context'] = f'\nOriginal Context: {state['context']}\nUser was not satisfied with the provided story, make improvements to your story component. User provided guidelines: {details}\n'

    return state
workflow.add_node("Follow Up", RunnableLambda(follow_up_node))


# def opt_human_node(state: AgentState):
#     if state["optional_human_nodes"]:
#         answer = input(f"\nApprove? (yes/no) \n").lower()
#         if 'yes' in answer or 'y' in answer:
#             state['routing'] = "yes"
#         elif 'no' in answer or 'n' in answer:
#             state['routing'] = "no"
#         else:
#             state['routing'] = "yes" 

#     return state 
# workflow.add_node("Optional Human Node", RunnableLambda(opt_human_node))

#### --- Specialized Agents ---
##### --- World ---
def world_builder_node(state: AgentState):
    print('\n\nGenerating..') #currently go through all agent nodes
    if 'world' in state["routing_list"]:
        print('     Building the World..')
        response = world_builder_agent(state["context"], persona=get_persona(persona='Worldbuilder'))
        state["world_outputs"].append(response)
        state["messages"].append({"role": "world_builder", "content": response})
    return state
workflow.add_node("World Builder", world_builder_node)

def world_builder_human_node(state: AgentState):
    if state["optional_human_nodes"]:
        print_state_message(state)
        # for msg in state["messages"][-1]["content"]:
        #     print(format_feedback(msg))

        
        answer = input(f"\n\nApprove? (yes/no) \n").lower()
        if 'yes' in answer or 'y' in answer:
            state['routing'] = "yes"
        elif 'no' in answer or 'n' in answer:
            state['routing'] = "no"
            new_context = input(f"\n\nWhat can be improved?\n").lower()
            state["context"] = f"Original direction: {state['context']} Updated user direction: {new_context}"
            # state["context"] = f"Original direction: {state['messages'][1]} Updated user direction: {new_context}" Original Context: {state['context']}
        else:
            state['routing'] = "yes" 
    return state 
workflow.add_node("Optional World Builder Human Node", RunnableLambda(world_builder_human_node))


##### --- Character ---
def character_dev_node(state: AgentState):
    if 'characters' in state["routing_list"]:
        print('     Developing Characters..')
        response = character_dev_agent(state["context"], persona=get_persona(persona='Archetype')) # only last output from world_builder , state["world_outputs"][-1]
        state["character_outputs"].append(response)
        state["messages"].append({"role": "character_developer", "content": response})
    return state
workflow.add_node("Character Developer", character_dev_node)

def character_dev_human_node(state: AgentState):
    if state["optional_human_nodes"]:
        print_state_message(state)
        # for msg in state["messages"][-1]["content"]:
        #     print(format_feedback(msg))

        answer = input(f"\n\nApprove? (yes/no) \n").lower()
        if 'yes' in answer or 'y' in answer:
            state['routing'] = "yes"
        elif 'no' in answer or 'n' in answer:
            state['routing'] = "no"
            new_context = input(f"\n\nWhat can be improved?\n").lower()
            state["context"] = f"Original direction: {state['context']} Updated user direction: {new_context}"
        else:
            state['routing'] = "yes" 

    return state 
workflow.add_node("Optional Character Dev Human Node", RunnableLambda(character_dev_human_node))

##### --- Plot ---
def plot_architect_node(state: AgentState):
    if 'plot' in state["routing_list"]:
        print('     Creating Plot & Story Arcs..')
        response = plot_architect_agent(state["context"], persona=get_persona(persona='Pacer')) # only last output , state["world_outputs"][-1], state["character_outputs"][-1]
        state["plot_outputs"].append(response)
        state["messages"].append({"role": "plot_architect", "content": response})
    return state
workflow.add_node("Plot Architect", plot_architect_node)

def plot_architect_human_node(state: AgentState):
    if state["optional_human_nodes"]:
        print_state_message(state)
        # for msg in state["messages"][-1]["content"]:
        #     print(format_feedback(msg))

        answer = input(f"\n\nApprove? (yes/no) \n").lower()
        if 'yes' in answer or 'y' in answer:
            state['routing'] = "yes"
        elif 'no' in answer or 'n' in answer:
            state['routing'] = "no"
            new_context = input(f"\n\nWhat can be improved?\n").lower()
            state["context"] = f"Original direction: {state['context']} Updated user direction: {new_context}"
        else:
            state['routing'] = "yes" 

    return state 
workflow.add_node("Optional Plot Architect Human Node", RunnableLambda(plot_architect_human_node))


##### --- Editor ---
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

##### --- Save State ---
def save_node(state: AgentState):
    save_graph_state(state, file_name='save_state')
    return state
workflow.add_node("Save Node", RunnableLambda(save_node))

### --- Edges ---
workflow.set_entry_point("Greeting Node")
workflow.add_edge("Greeting Node", "World Builder")

workflow.add_edge("World Builder", "Optional World Builder Human Node")
workflow.add_conditional_edges(
    "Optional World Builder Human Node", # source node
    lambda s: s.get("routing", "yes"),
    {"yes": "Character Developer", "no": "World Builder"}
)

workflow.add_edge("Character Developer", "Optional Character Dev Human Node")
workflow.add_conditional_edges(
    "Optional Character Dev Human Node", # source node
    lambda s: s.get("routing", "yes"),
    {"yes": "Plot Architect", "no": "Character Developer"}
)

workflow.add_edge("Plot Architect", "Optional Plot Architect Human Node")
workflow.add_conditional_edges(
    "Optional Plot Architect Human Node", # source node
    lambda s: s.get("routing", "yes"),
    {"yes": "Head Writer", "no": "Plot Architect"}
)

workflow.add_edge("Head Writer", "Human Node")
workflow.add_conditional_edges(
    "Human Node", # source node
    lambda s: s.get("routing", "yes"),
    {"yes": "Save Node", "no": "Follow Up"}
)

workflow.add_edge("Save Node", END)
workflow.add_edge("Follow Up", "World Builder")

app = workflow.compile()

