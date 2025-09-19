


from langchain_ollama import ChatOllama
# from langchain.agents import initialize_agent
# from langchain.schema import SystemMessage
from langchain.agents import AgentExecutor, create_react_agent
from langgraph.graph import StateGraph, END
from langgraph.graph.state import MessagesState
from langchain_core.prompts import PromptTemplate

# ---- 1. Local LLM ----
llm = ChatOllama(model="gemma3", temperature=0.7)

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


# ---- 3. Creative Agents (react) ----

# -------- a. World Builder --------
# tools_a = tools
prompt=""
world_builder = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=world_builder, tools=tools)

agent_executor.invoke({"input": "hi"})

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

# ---- 4. Showrunner Node (Manager) ----
def showrunner_node(state: MessagesState):
    user_prompt = state["messages"][-1].content
    print(f"\n[Showrunner] Prompt: {user_prompt}")

    # Call agents sequentially (each call will be traced in LangSmith)
    world = world_builder.run(user_prompt)
    # chars = character_dev.run(user_prompt)
    # plot  = plot_architect.run(user_prompt)
    # style = stylist.run(user_prompt)

    combined_draft = (
        f"---World---\n{world}\n\n"
        # f"---Characters---\n{chars}\n\n"
        # f"---Plot---\n{plot}\n\n"
        # f"---Style---\n{style}"
    )

    critique = editor_critic.run(
        "Review the following creative material and provide feedback:\n" + combined_draft
    )

    final = (
        "🎬 **Creative Writer's Room Output** 🎬\n"
        + combined_draft
        + "\n\n---Editor/Critic Feedback---\n"
        + critique
    )
    return {"messages": state["messages"] + [{"role": "system", "content": final}]}

# ---- 5. LangGraph Workflow ----
workflow = StateGraph(MessagesState)
workflow.add_node("Showrunner", showrunner_node)
workflow.set_entry_point("Showrunner")
workflow.add_edge("Showrunner", END)
app = workflow.compile()

# ---- 6. Run Session ----
if __name__ == "__main__":
    prompt = "Develop a dark fantasy world about a city floating above a poisonous sea."
    result = app.invoke({"messages": [{"role": "user", "content": prompt}]})
    print("\nFINAL CREATIVE PACKAGE:\n")
    print(result["messages"][-1]["content"])
