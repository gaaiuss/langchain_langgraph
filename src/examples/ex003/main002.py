import operator
from dataclasses import dataclass
from typing import Annotated, Literal

from langgraph.graph import StateGraph
from rich import print


@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0


def node_a(state: State) -> State:
    output_state: State = State(nodes_path=["A"], current_number=state.current_number)
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state


def node_b(state: State) -> State:
    output_state: State = State(nodes_path=["B"], current_number=state.current_number)
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state


def node_c(state: State) -> State:
    output_state: State = State(nodes_path=["C"], current_number=state.current_number)
    print("> node_c", f"{state=}", f"{output_state=}")
    return output_state


# Conditional function
def the_conditional(state: State) -> Literal["goes_to_b", "goes_to_c"]:
    if state.current_number >= 50:  # noqa: PLR2004
        return "goes_to_c"
    return "goes_to_b"


builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

builder.add_edge("__start__", "A")
builder.add_conditional_edges(
    "A", the_conditional, {"goes_to_b": "B", "goes_to_c": "C"}
)
builder.add_edge("B", "__end__")
builder.add_edge("C", "__end__")

graph = builder.compile()
print(graph.get_graph().draw_mermaid_png(output_file_path="graph.png"))

print()
response = graph.invoke(State(nodes_path=[]))
print(f"{response=}")
print()


print()
response = graph.invoke(State(nodes_path=[], current_number=51))
print(f"{response=}")
print()
