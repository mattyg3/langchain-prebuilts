from llm_init import llm

def plot_architect_agent(story_idea: str, world_output: str, character_output: str):

    prompt = f"""
    # Role
    You are a Plot Architect. 

    # Task
    Given these story components (World Design, Characters), develop an interesting plot for a novel. Include the total story arc and key conflicts. 
    
    # Inputs
    Story Concept: {story_idea}
    World Design: {world_output}
    Characters: {character_output}

    # Output
    An organized plot, story arc, and key conflicts. **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")