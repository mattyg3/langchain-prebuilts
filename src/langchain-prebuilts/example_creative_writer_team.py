import llm_init # Needed to track traces with langsmith
import workflows.creative_writing_room.compile_workflow 
from workflows.creative_writing_room.compile_workflow import app, create_agent_state  #AgentState,
from util_funcs import save_graph_viz, get_plot #, format_feedback

# ---- Interactive Session ----
if __name__ == "__main__":

    #Get Plot Archetype
    plot_doc = get_plot("Antihero Journey")

    # Initialize an empty state
    state = create_agent_state(context=f'Plot Archetype: {str(plot_doc)}\n')

    # Save graph diagram to folder
    save_graph_viz(app) #file_name='saved_langgraph_viz'

    # Initial full pipeline run
    state = app.invoke(state) #saves state to file_name='saved_state_'+timestamp