import llm_init # Needed to track traces with langsmith
from util_funcs import get_plot, parse_plot_doc, save_run
import workflows.algo_solver.compile_workflow 
from workflows.algo_solver.compile_workflow  import app, create_agent_state


# # ---- Interactive Session ----
# if __name__ == "__main__":
