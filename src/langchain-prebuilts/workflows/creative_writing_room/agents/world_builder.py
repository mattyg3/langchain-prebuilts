from llm_init import llm_high_temp as llm

def world_builder_agent(story_idea: str, persona=None):

    prompt = f"""
    # Role
    You are a World Builder. 
    
    # Personality (Optional Input)
    Your personality: {persona}

    # Task
    Given the Story Concept, create a detailed setting including lore, religion, time period, location(s), and additional cultural details.
    
    # Inputs
    Story Concept: {story_idea}

    # Output - **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**

    A detailed and organized description of the created world. 

    ## Output Format - **Detailed Overview of created World**
        ### Short Example Detailed Overview, write your own sections based on the created World.
    ```
    # World Name
    ## Setting
    **Desciption of the World's setting**
    ## Technology
    **Description of technology level and specific tech available**
    ## Lore
    **Description of World's lore**

    ```
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")