from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0.7, validate_model_on_init=True)

def editor_critic_agent(story_idea: str, world_output: str, character_output: str, plot_output: str):

    prompt = f"""
    You are an Editor/Critic. For the desired story: {story_idea}, provide critical feedback for each of the main components:
    - World Design: {world_output}
    - Characters: {character_output}
    - Plot: {plot_output}

    For each of these components, give suggestions for improvement if necessary. 
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")