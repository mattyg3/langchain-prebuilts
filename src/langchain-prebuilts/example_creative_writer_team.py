import llm_init # Needed to track traces with langsmith
import workflows.creative_writing_room.compile_workflow 
from workflows.creative_writing_room.compile_workflow import app, create_agent_state #AgentState,
from util_funcs import save_graph_viz #, format_feedback

# ---- Interactive Session ----
if __name__ == "__main__":
    # prompt = "Develop a story about an Atlantis type civilization. An early plot point should be a catastrophic event, resulting in our characters needing to learn how to survive without their advanced technology."
    # prompt = "Create a simple short story about a fisherman in the Midwest US."
    # prompt = "Develop a Hero's Journey type story about an outcast male teenager. Story should take place in a high-fantasy world."
    # prompt = "Develop a story about a fictional small town in the south US, during a zombie apocalypse"
    # state = create_agent_state(messages=[{"role": "user", "content": prompt}], context={"story_idea": prompt})

    # Initialize an empty state
    state = create_agent_state()

    # Save graph diagram to folder
    save_graph_viz(app, 'src/langchain-prebuilts/workflows/creative_writing_room/langgraph_diagram')

    # Initial full pipeline run
    state = app.invoke(state)