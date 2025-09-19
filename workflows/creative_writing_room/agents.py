import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = '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'

from langchain_ollama import ChatOllama
# from langchain.agents import initialize_agent
# from langchain.schema import SystemMessage
from langchain.agents import AgentExecutor, create_react_agent
from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.prompts import PromptTemplate
# from langgraph import LLMNode


from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated, TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime


from langchain_core.runnables import RunnableConfig, RunnableLambda

# ---- 1. Local LLM ----
llm = ChatOllama(model="gemma3:4b", temperature=0.7, validate_model_on_init=True)

# Reducer collects outputs from agents
def append_output(a: list, b: str | None) -> list:
    if b is not None:
        return a + [b]
    return a
# Define State and Context
# -------------------------
class State(TypedDict):
    world_outputs: Annotated[list, append_output]
    character_outputs: Annotated[list, append_output]
    plot_outputs: Annotated[list, append_output]
    editor_feedback: Annotated[list, append_output]
    messages: Annotated[list, append_output]

class Context(TypedDict):
    story_idea: str



# # ---- 2. Helper to create specialized agents ----
# def make_agent(role_description):
#     return initialize_agent(
#         tools=[],  # Add tools if needed
#         llm=llm,
#         agent="chat-zero-shot-react-description",
#         verbose=True,
#         system_message=SystemMessage(
#             content=(
#                 f"You are the {role_description}. "
#                 "Provide rich, detailed creative content."
#             )
#         ),
#     )

# ---- 2. Define Tools ----
tools=[]
def dummytool() -> None:
    """Testing tool."""
    ...
tools.append(dummytool)


# ---- 3. Creative Agents (react) ----

# -------- a. Editor/Critic --------
system_prompt = "You are an Editor/Critic. Provide critical feedback. "
if system_prompt:
    preprocessor = RunnableLambda(
        lambda state: [{"role": "system", "content": system_prompt}]
        + state["messages"]
    )
else:
    preprocessor = RunnableLambda(
        lambda state: state["messages"]
    )
critic_runnable = preprocessor | llm
def call_critic(state: State, config: RunnableConfig):
    response = critic_runnable.invoke(state, config)
    return {"messages": [response], "editor_feedback": [response]}
# def editor_critic_node(state: State, runtime: Runtime[Context]) -> dict:
#     # last_plot = state["plot_outputs"][-1]
#     last_world = state["world_outputs"][-1]
#     llm.invoke()
#     # last_characters = state["character_outputs"][-1]
#     feedback = f"Editor feedback on plot:  world: {last_world}" #, characters: {last_characters}, {last_plot}
#     return {"editor_feedback": feedback}
# editor_critic = LLMNode(name="Editor/Critic", model=llm, prompt="""
# You are an Editor/Critic. Provide critical feedback. 
# """
# )
# tools_a = tools
# prompt = PromptTemplate.from_template("Editor/Critic: a review and suggest improvements")
# editor_critic = create_react_agent(llm, tools, prompt)
# editor_critic_executor = AgentExecutor(agent=editor_critic, tools=tools)

# -------- b. World Builder --------
system_prompt = """You are a World Builder. 
Given the story idea: {story_idea}, 
create a detailed setting including time period, locations, and cultural aspects."""
if system_prompt:
    preprocessor = RunnableLambda(
        lambda state: [{"role": "system", "content": system_prompt}]
        + state["messages"]
    )
else:
    preprocessor = RunnableLambda(
        lambda state: state["messages"]
    )
world_builder_runnable = preprocessor | llm
def call_world_builder(state: State, config: RunnableConfig):
    response = world_builder_runnable.invoke(state, config)
    return {"messages": [response], "world_outputs": [response]}
# def world_builder_node(state: State, runtime: Runtime[Context]) -> dict:
#     idea = runtime.context["story_idea"]
#     # Here you would call LLM, simplified as a string for demo
#     world_text = f"World built for idea: {idea}"
#     return {"world_outputs": world_text}
# world_builder = LLMNode(name="World Builder", model=llm, prompt="""
# You are a World Builder. 
# Given the story idea: {story_idea}, 
# create a detailed setting including time period, locations, and cultural aspects.
# """
# )
# tools_a = tools
# prompt = PromptTemplate.from_template("World Builder: create immersive settings and lore")
# world_builder = create_react_agent(llm, tools, prompt)
# world_builder_executor = AgentExecutor(agent=world_builder, tools=tools)
# agent_executor.invoke({"input": "hi"})

# # Use with chat history
# from langchain_core.messages import AIMessage, HumanMessage
# agent_executor.invoke(
#     {
#         "input": "what's my name?",
#         # Notice that chat_history is a string
#         # since this prompt is aimed at LLMs, not chat models
#         "chat_history": "Human: My name is Bob\nAI: Hello Bob!",
#     }
# )

# world_builder  = make_agent("World Builder: create immersive settings and lore")
# character_dev  = make_agent("Character Developer: invent characters and motivations")
# plot_architect = make_agent("Plot Architect: craft story arcs and conflicts")
# stylist        = make_agent("Stylist: recommend tone, diction, and narrative style")
# editor_critic  = make_agent("Editor/Critic: review and suggest improvements")

# # ---- 4. Showrunner Node (Manager) ----
# def showrunner_node(state: MessagesState):
#     user_prompt = state["messages"][-1].content
#     print(f"\n[Showrunner] Prompt: {user_prompt}")

#     # Call agents sequentially (each call will be traced in LangSmith)
#     # world = world_builder.run(user_prompt)
#     world = world_builder_executor.invoke({"input": user_prompt})
#     # chars = character_dev.run(user_prompt)
#     # plot  = plot_architect.run(user_prompt)
#     # style = stylist.run(user_prompt)
    

#     combined_draft = (
#         f"---World---\n{world}\n\n"
#         # f"---Characters---\n{chars}\n\n"
#         # f"---Plot---\n{plot}\n\n"
#         # f"---Style---\n{style}"
#     )

#     # critique = editor_critic.run(
#     #     "Review the following creative material and provide feedback:\n" + combined_draft
#     # )

#     critique = editor_critic_executor.invoke({"input": f"Review the following creative material and provide feedback:\n{combined_draft}"})

#     final = (
#         "🎬 **Creative Writer's Room Output** 🎬\n"
#         + combined_draft
#         + "\n\n---Editor/Critic Feedback---\n"
#         + critique
#     )
#     return {"messages": state["messages"] + [{"role": "system", "content": final}]}

# # ---- 5. LangGraph Workflow ----
# workflow = StateGraph(MessagesState)
# workflow.add_node("Showrunner", showrunner_node)
# workflow.set_entry_point("Showrunner")
# workflow.add_edge("Showrunner", END)
# app = workflow.compile()
workflow = StateGraph(state_schema=State, context_schema=Context)
workflow.add_node("World Builder", RunnableLambda(call_world_builder))
# workflow.add_node("Character Developer", character_developer_node)
# workflow.add_node("Plot Architect", plot_architect_node)
workflow.add_node("Editor/Critic", RunnableLambda(call_critic))
workflow.set_entry_point("World Builder")
workflow.set_finish_point("Editor/Critic")
workflow.add_edge("World Builder", "Editor/Critic")

compiled = workflow.compile()

story_idea = "A young explorer discovers a hidden magical kingdom in the mountains."

result = compiled.invoke(
    {"world_outputs": [],  "editor_feedback": []}, #"character_outputs": [], "plot_outputs": [],
    context={"story_idea": story_idea}
)

print(result)

# # ---- 6. Run Session ----
# if __name__ == "__main__":
#     prompt = "Develop a dark fantasy world about a city floating above a poisonous sea."
#     result = app.invoke({"messages": [{"role": "user", "content": prompt}]})
#     print("\nFINAL CREATIVE PACKAGE:\n")
#     print(result["messages"][-1]["content"])
