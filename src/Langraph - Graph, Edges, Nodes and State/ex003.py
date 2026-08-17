import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph
from rich import print


# 1. Define node state typing (TypedDict)
class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add]


# 2. Define the nodes
def node_a(state: State) -> State:
    output_state: State = {"nodes_path": ["A"]}
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state


def node_b(state: State) -> State:
    output_state: State = {"nodes_path": ["B"]}
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state


# 3. Define graph builder
builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)

# 4. Connect edges
builder.add_edge("__start__", "A")
builder.add_edge("A", "B")
builder.add_edge("B", "__end__")

# 5. Compile graph
graph = builder.compile()

# See the graph
# graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 6. Get result
response = graph.invoke({"nodes_path": []})

# Get all the result
print()
print(f"{response=}")
print()
