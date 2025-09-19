from llm_init import llm

def editor_critic_agent(story_idea: str, world_output: str, character_output: str, plot_output: str):

    prompt = f"""
    # Role
    You are an Editor/Critic. 

    # Task
    Provide critical feedback for each of the main story components (World Design, Characters, and Plot)
    
    # Inputs
    Story Concept: {story_idea}
    World Design: {world_output}
    Characters: {character_output}
    Plot: {plot_output}

    # Output
    An organized review of the main story components. Give suggestions for improvement if necessary. **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")