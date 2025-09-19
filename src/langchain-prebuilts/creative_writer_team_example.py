import langsmith_link #Needed to track traces with langsmith
# from workflows.creative_writing_room.agents import * #Import Agents
import workflows.creative_writing_room.compile_workflow 
from workflows.creative_writing_room.compile_workflow import app, AgentState, run_selected_agents
from util_funcs import format_feedback

# print()
# print(agents)
# ---- Interactive Session ----
if __name__ == "__main__":
    prompt = "Develop a story about an Atlantis type civilization. An early plot point should be a catastrophic event, resulting in our characters needing to learn how to survive without their advanced technology."

    state: AgentState = {
        "messages": [{"role": "user", "content": prompt}],
        "context": {"story_idea": prompt},
        "world_outputs": [],
        "character_outputs": [],
        "plot_outputs": [],
        "editor_feedback": [],
        "head_writer_outputs": [],
    }

    # Initial full pipeline run
    state = app.invoke(state)
    print("\nFINAL CREATIVE PACKAGE:\n")
    for chunk in state["head_writer_outputs"]:
        print(format_feedback(chunk))

    while True:
        follow = input("\n[Follow-up] Enter more questions/ideas (or 'exit'): ").strip()
        if follow.lower() in {"exit", "quit", "done", "finished"}:
            print("Session ended.")
            break

        state["messages"].append({"role": "user", "content": follow})
        state["context"]["story_idea"] = follow  # optional: treat as new seed

        choice = input(
            "Which agents to rerun? "
            "[a]ll, [w]orld, [c]haracter, [p]lot, [e]ditor (e.g. wc): "
        ).strip().lower()

        if choice in {"a", ""}:
            # Empty or 'a' => full run
            state = app.invoke(state)
        else:
            # Dependency-aware partial run
            state = run_selected_agents(state, list(choice))

        print("\nUPDATED CREATIVE PACKAGE:\n")
        for chunk in state["head_writer_outputs"]:
            print(format_feedback(chunk))
