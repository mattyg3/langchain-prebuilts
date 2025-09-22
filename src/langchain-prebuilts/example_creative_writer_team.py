import llm_init # Needed to track traces with langsmith
import workflows.creative_writing_room.compile_workflow 
from workflows.creative_writing_room.compile_workflow import app, create_agent_state  #AgentState,
from util_funcs import get_plot, parse_plot_doc, save_run #, format_feedback save_graph_viz, 

# ---- Interactive Session ----
if __name__ == "__main__":

    #Get Plot Archetype
    plot_doc = parse_plot_doc(get_plot("Tragedy of Forbidden Love"))

    # Initialize an empty state
    state = create_agent_state(optional_human_nodes=False, context=f'{str(plot_doc)}\n')

    
    # save_graph_viz(app) #file_name='saved_langgraph_viz'

    # Initial full pipeline run
    state = app.invoke(state) #saves state to file_name='saved_state_'+timestamp
    # print('\n\n')
    # print(type(state))

    # Save graph diagram to folder
    save_run(state, app, run_name='dev_run1', save_path='src/langchain-prebuilts/outputs')