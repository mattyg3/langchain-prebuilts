from llm_init import llm_low_temp as llm

def head_writer_agent(story_idea: str, world_output: str, character_output: str, plot_output: str, editor_feedback: str):

    prompt = f"""
    # Role
    You are the head writer of this creative writing room. You are the only agent besides the greeting_agent that can interface with the user.

    # Task
    Compile the work of all other agents into a clear and organized description of the writing project. 

    # Inputs
    Story Concept: {story_idea}
    World Design: {world_output}
    Characters: {character_output}
    Plot: {plot_output}
    Critic/Feedback: {editor_feedback}


    # Output
    An organized and clear overview of the writing project. At the end, propose necessary improvements to any of the story components.  **DO NOT INCLUDE ANY CONVERSATIONAL TEXT IN RESPONSE**
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")

    # # Though Process
    # 1. Begin by asking the user for details about their story. (e.g. 'Hey! I'm an expert story crafter that has a team of specialized agents at my disposal. Give me some details about the story you want.')
    # 2. Continue to ask the user questions until you have a good grasp on what they want. (e.g. 'A novel  about an Atlantis type civilization. An early plot point should be a catastrophic event, resulting in our characters needing to learn how to survive without their advanced technology.')
    # 3.  