# import os
# # os.environ["LANGSMITH_PROJECT"] = "creative_writing_team"
# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_API_KEY"] = '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'

from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0.7, validate_model_on_init=True)

def world_builder_agent(story_idea: str):

    prompt = f"""
    You are a World Builder. 
    Given the story idea: {story_idea}, 
    create a detailed setting including time period, locations, and cultural aspects.
    """
    response = llm.invoke(prompt)
    return response.content.split("\n")