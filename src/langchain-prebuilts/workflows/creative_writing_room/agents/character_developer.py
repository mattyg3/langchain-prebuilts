from llm_init import llm_high_temp as llm

def character_dev_agent(story_idea: str): #, world_output: str

    prompt = f"""
    # Role
    You are a Character Development Specialist. 

    # Task
    Given these story components (Story Concept), develop a set of characters the story will revolve around. Include personality traits and underlying character motivations. 
    
    # Inputs
    Story Concept: {story_idea}
 

    # Output
    An organized list of characters with key details. **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")

#   World Design: {world_output}