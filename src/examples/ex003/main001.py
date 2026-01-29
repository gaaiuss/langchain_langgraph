import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph
from rich import print


# 1 - Define state
class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add]


# 2 - Define nodes
def a_node(state: State) -> State:
    output_state: State = {"nodes_path": ["A"]}
    print("> a_node", f"{state=}", f"{output_state=}")
    return output_state


def b_node(state: State) -> State:
    output_state: State = {"nodes_path": ["B"]}
    print("> b_node", f"{state=}", f"{output_state=}")
    return output_state


# 3 - Graph builder
builder = StateGraph(State)

builder.add_node("A", a_node)
builder.add_node("B", b_node)

# 4 - Connect edges
builder.add_edge("__start__", "A")
builder.add_edge("A", "B")
builder.add_edge("B", "__end__")

# 5 - Compile graph
graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path="file.png")
# print(graph.get_graph().draw_mermaid()) # another option to see the graph

# Get result
response = graph.invoke({"nodes_path": []})

print()
print(f"{response=}")
print()
