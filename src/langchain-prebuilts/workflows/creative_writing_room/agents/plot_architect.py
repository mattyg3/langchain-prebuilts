from llm_init import llm

def plot_architect_agent(story_idea: str, plot_arch=[]): # , world_output: str, character_output: str

    ## add plot_arch logic here...

    prompt = f"""
    # Role
    You are a Plot Architect. 

    # Task
    Given the Story Concept, develop an interesting plot for a novel. Include the total story arc and key conflicts. 
    
    # Inputs
    Story Concept: {story_idea}


    # Output - **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**

    An organized plot, story arc, and key conflicts. 

    ## Output Format - **Plot Summary & Plot Outline**
    ```
    # Plot Summary
    **Plot Summary (1 or 2 paragraphs)**

    # Plot Outline
    **Outline of Plot, breakdown down to Acts level of Plot**

    ```

    """
    response = llm.invoke(prompt)
    return response.content.split("\n")

    # World Design: {world_output}
    # Characters: {character_output}