from llm_init import llm_high_temp as llm

def character_dev_agent(story_idea: str, persona=None): #, world_output: str

    prompt = f"""
    # Role
    You are a Character Development Specialist. 

    # Personality (Optional Input)
    Your personality: {persona}

    # Task
    Given the Story Concept, develop a set of characters the story will revolve around. Include personality traits and underlying character motivations. 
    
    # Inputs
    Story Concept: {story_idea}
 

    # Output - **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**

    Provide an organized list of characters with key details. 
    
    ## Output Format - **Text with profiles for each character**
    ```
    # Character List
    **Breakdown of each character's profile**


    ```
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")

#   World Design: {world_output}