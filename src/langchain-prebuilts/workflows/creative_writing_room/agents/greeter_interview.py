from llm_init import llm_low_temp as llm

def greeting_agent(answer):

    prompt = f"""
    # Role - Greeter
    You are the first point of contact with the user. You are the only agent besides the head_writer_agent that can interface with the user.

    # Task
    Gather details from the user about the desired story into a dict to be used as context for another LLM. 

    # Input
    Story Description: {answer}

    # Output - **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**

    ## Output Format - **dict like string**
    ### Example dict contents, create your own dict key/value pairs based on the user input.
    ```
    "setting": ,
    "technology_level": ,
    "cultural_details": ,
    ```

    """
    response = llm.invoke(prompt)
    return response.content.split("\n")

    # # Though Process
    # 1. Begin by asking the user for details about their story. (e.g. 'Hey! I'm an expert story crafter that has a team of specialized agents at my disposal. Give me some details about the story you want.')
    # 2. Continue to ask the user questions until you have a good grasp on what they want. (e.g. 'A novel  about an Atlantis type civilization. An early plot point should be a catastrophic event, resulting in our characters needing to learn how to survive without their advanced technology.')
    # 3.  You must continue to ask questions until you can return a completed dict.