##PRINT FUNCTIONS##
def format_feedback(raw_text: str) -> str:
    """
    Format a long feedback string into a clean, easy-to-read block
    with line wrapping, bullet alignment, and spacing.

    Args:
        raw_text (str): The raw feedback text.

    Returns:
        str: Nicely formatted feedback ready to print or save.
    """
    import textwrap

    # Normalize newlines and strip extra spaces
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    formatted_lines = []
    wrapper = textwrap.TextWrapper(width=80, subsequent_indent="    ")

    for line in lines:
        # Section headers
        if line.startswith("**") and line.endswith("**"):
            title = line.strip("* ")
            formatted_lines.append("\n" + "=" * 60)
            formatted_lines.append(title.upper())
            formatted_lines.append("=" * 60 + "\n")
        # Sub-bullets
        elif line.startswith("*"):
            bullet_text = line.lstrip("* ").strip()
            formatted_lines.append("- " + bullet_text)
        # Indented bullets
        elif line.startswith("    *"):
            sub_text = line.lstrip("* ").strip()
            formatted_lines.append("    • " + sub_text)
        else:
            # Wrap normal text
            wrapped = wrapper.fill(line)
            formatted_lines.append(wrapped)

    return "\n".join(formatted_lines)


##SAVE FUNCTIONS##
import json
from pathlib import Path
from datetime import datetime
def save_graph_viz(graph, file_name='saved_langgraph_viz', parent_path='src/langchain-prebuilts/outputs'):
    #Set PATH for graphviz
    import os
    os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

    #Save Path
    save_path = Path(f'{parent_path}/{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    from graphviz import Digraph
    # --- Export to Graphviz ---
    dot = Digraph(comment="LangGraph Workflow")

    # Add nodes and edges
    for node in graph.get_graph().nodes:
        dot.node(node, node)

    for edge in graph.get_graph().edges:
        dot.edge(edge[0], edge[1])

    # Save to a PNG inside the workspace 'src\langchain-prebuilts\workflows\creative_writing_room'
    dot.render(save_path, format="png", cleanup=True)


def save_graph_state(state, file_name='saved_state', parent_path='src/langchain-prebuilts/outputs'):
    #Save Path
    save_path = Path(f'{parent_path}/{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w") as f:
        json.dump(state, f, indent=4)