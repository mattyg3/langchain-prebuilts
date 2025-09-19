from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0.7, validate_model_on_init=True)

def character_dev_agent(story_idea: str, world_output: str):

    prompt = f"""
    # Role
    You are a Character Development Specialist. 

    # Task
    Given these story components (World Design), develop a set of characters the story will revolve around. Include personality traits and underlying character motivations. 
    
    # Inputs
    Story Concept: {story_idea}
    World Design: {world_output}

    # Output
    An organized list of characters with key details. **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")