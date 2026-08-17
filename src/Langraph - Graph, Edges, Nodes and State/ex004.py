"""Graph with conditional edges"""

import operator
from dataclasses import dataclass
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from rich import print


# As a dataclass it will be the same ideia, the difference is that the dataclass
# will help you inside the nodes but the return will be a dict as always.
@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    # This number will be used to control the state number that will be used
    # by the conditional function `the_conditional`
    current_state_number: int = 0


def node_a(state: State) -> State:
    output_state: State = State(
        nodes_path=["A"],
        current_state_number=state.current_state_number,
    )
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state


def node_b(state: State) -> State:
    output_state: State = State(
        nodes_path=["B"],
        current_state_number=state.current_state_number,
    )
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state


def node_c(state: State) -> State:
    output_state: State = State(
        nodes_path=["C"],
        current_state_number=state.current_state_number,
    )
    print("> node_c", f"{state=}", f"{output_state=}")
    return output_state


# Conditional function
# This is the function that represents the conditional edge, it returns the literal
# node that will be called next.
def the_conditional(state: State) -> Literal["goes_to_b", "goes_to_c"]:
    if state.current_state_number >= 50:  # noqa: PLR2004
        # the name here is different because we are talking about the edges itself.
        return "goes_to_c"  # name of the edge
    return "goes_to_b"  # name of the edge


builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

builder.add_edge(START, "A")  # START: same as "__start__"
# As for this example, after the node A we will go to B or C, so that is why we
# use the conditional edge here.
builder.add_conditional_edges(
    "A",  # source
    the_conditional,  # conditional function
    # teaching the result of the condition to the conditional function
    {
        # the first is the edge name and the second the node name
        "goes_to_b": "B",
        "goes_to_c": "C",
    },
)
builder.add_edge("B", END)  # END: same as "__end__"
builder.add_edge("C", END)  # END: same as "__end__"

graph = builder.compile()

print()
response = graph.invoke(State(nodes_path=[]))
print(f"{response=}")
print()


print()
# Testing the condition inside the conditional function
response = graph.invoke(State(nodes_path=[], current_state_number=51))
print(f"{response=}")
print()
