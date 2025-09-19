from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0.7, validate_model_on_init=True)

def plot_architect_agent(story_idea: str, world_output: str, character_output: str):

    prompt = f"""
    You are a Plot Architect. 
    Given the story idea: {story_idea}, world description: {world_output}, and characters: {character_output}
    Develop an interesting plot for a novel. Include the total story arc and key conflicts.  
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")