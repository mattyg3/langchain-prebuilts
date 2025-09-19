from llm_init import llm_low_temp as llm

def head_writer_agent(story_idea: str, world_output: str, character_output: str, plot_output: str, editor_feedback: str):

    prompt = f"""
    # Role
    You are the head writer of this creative writing room. 

    # Task
    Compile the work of all other agents, and output a clear and organized description of the writing project. 

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