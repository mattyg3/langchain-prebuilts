from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0.7, validate_model_on_init=True)

def world_builder_agent(story_idea: str):

    prompt = f"""
    # Role
    You are a World Builder.  

    # Task
    Given the story concept, create a detailed setting including time period, locations, and cultural details.
    
    # Inputs
    Story Concept: {story_idea}

    # Output
    A detailed and organized description of the created world. **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")