
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
    # Set PATH for graphviz
    import os
    os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

    # Save Path
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
    # Save Path
    save_path = Path(f'{parent_path}/{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w") as f:
        json.dump(state, f, indent=4) #.model_dump()

def save_agent_outputs(state, file_name='saved_summary_doc', parent_path='src/langchain-prebuilts/outputs'):
    # Save Path
    save_path = Path(f'{parent_path}/{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Combine Agents outputs
    content = f"OUTPUT\n\n{state['head_writer_outputs'][-1]}\n\n{state['world_outputs'][-1]}\n\n{state['character_outputs'][-1]}\n\n{state['plot_outputs'][-1]}\n\n"
    # content = f"OUTPUT\n\n{state['head_writer_outputs']}\n\n{state['world_outputs']}\n\n{state['character_outputs']}\n\n{state['plot_outputs']}\n\n"

    with open(save_path, "w", encoding="utf-8") as f: #"a" for append
        f.write(content)

def create_unique_folder(base_name: str, parent: str = ".") -> Path:
    """
    Create a folder with base_name inside parent directory.
    If it exists, create a variant like base_name_1, base_name_2, etc.
    Returns the final Path.
    """
    parent_path = Path(parent)
    folder = parent_path / base_name
    counter = 1

    while folder.exists():
        folder = parent_path / f"{base_name}_REV{counter}"
        counter += 1

    folder.mkdir(parents=True)
    return folder

def save_run(state, graph, run_name='unnamed_run', save_path='src/langchain-prebuilts/outputs'):
    # #Set PATH for graphviz
    # import os
    # os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

    # Create Output Folder if none exists
    Path(f'{save_path}/{run_name}').parent.mkdir(parents=True, exist_ok=True)

    # Create Run Folder, If already exists, create a REV
    run_folder = create_unique_folder(base_name=run_name, parent=save_path)

    # Save Graph State
    save_graph_state(state, parent_path=run_folder)

    # Save Graph Visual
    save_graph_viz(graph, parent_path=run_folder)

    # Save Agent Output Doc
    save_agent_outputs(state, parent_path=run_folder)

    print(f"\n\n    ..Saved to: {run_folder}\n")

    


##WRITING PERSONALITIES##
def view_persona_options(file_path = 'src/langchain-prebuilts/util_data/personalities.json'):
    ####Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #### Access the list of agents
    agents = data["agents"]

    #### Example: print all agent names
    for agent in agents:
        print(agent["name"], "-", agent["role"])
        print(agent["description"], "\n")

def get_persona(persona, file_path = 'src/langchain-prebuilts/util_data/personalities.json'):
    ####Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #### Access the list of agents
    agents = data.get("agents")
    for doc in agents:
        agent = doc.get("name")
        if agent.lower() == persona.lower():
            return doc
        else:
            pass
    return None

##ARCHETPYES##
def view_plot_archetypes(file_path = 'src/langchain-prebuilts/util_data/plot_archetypes.json'):
    ####Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #### Access the list of plot_archetypes
    plots = data["plot_archetypes"]

    #### Example: print all agent names
    for plot in plots:
        print(plot["name"], "-", plot["description"], "\n")

def get_plot(plot, file_path = 'src/langchain-prebuilts/util_data/plot_archetypes.json'):
    ####Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #### Access the list of plot_archetypes
    plots = data.get("plot_archetypes")
    for doc in plots:
        agent = doc.get("name")
        if agent.lower() == plot.lower():
            return doc
        else:
            pass
    return None

def parse_plot_doc(doc):
    return f"Plot Archetype: \n   Name: {doc['name']} \n   Description: {doc['description']} \n   Key Elements: {doc['key_elements']}\n"