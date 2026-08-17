"""Langgraph

For more complex applications, which demands back to back or execute and return
to a previous step, we use the graphs models.

Instead of chain calls in a hard applicated way, we work as a graph format.
This means that we use nodes conected by edges.

Nodes: functions that executes certain single actions (LLM call for example).
Edges: determine which node will be executed next. They can also be conditional.

When creating a new graph project, it is for the best pratice to write down the
nodes and edges on a other source than just writing code without thinking or
how the graph will look like.

Template builder: build.langchain.com

Minimum requirements to create a Graph:
    - State: defines the graph state, which will be the entire data structure that
    will be used in the entire graph (It can be a TypedDict, a dataclass or a
    Pydantic model).
    - Nodes: functions that receive the state as an input, execute actions and
    return the updated state.
    - Edges: node conections that can be simple or conditional.
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph
from rich import print


# 1. Define node state (TypedDict or dataclass)
class State(TypedDict):
    # for each node executed, it will store the path in a list[str]
    # nodes_path: list[str]

    """
    For this case, the correct way is to use Annotated with what they call a
    reducer. The reducer basically gets the output from the previous nodes and
    join them in another state, as showed in the example function bellow.
    """

    # def reducer(a: list[str], b: list[str]) -> list[str]:
    #     return a + b
    # nodes_path: Annotated[list[str], reducer]

    # nodes_path: Annotated[list[str], lambda a, b: a + b]
    # In the case bellow the operator.add does the same thing as the lambda
    # function atop.
    nodes_path: Annotated[list[str], operator.add]


# 2. Create the nodes
def node_a(state: State) -> State:
    """
    In the nodes you do not change the state directly, you will always return
    a new state.
    """
    # nodes_path = state["nodes_path"]  # or input state
    # output_state: State = {"nodes_path": [*nodes_path, "A"]}

    # In normal circunstances we always return a new state with only the proper
    # output from the node
    output_state: State = {"nodes_path": ["A"]}  # we want only the return of A
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state


def node_b(state: State) -> State:
    # nodes_path = state["nodes_path"]  # or input state
    # output_state: State = {"nodes_path": [*nodes_path, "B"]}
    output_state: State = {"nodes_path": ["B"]}  # we want only the return of B
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state


# 3. Define graph builder
builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)

# 4. Create the edges
builder.add_edge("__start__", "A")  # conects start to node_a
builder.add_edge("A", "B")  # conects node_a to node_b
builder.add_edge("B", "__end__")  # conects node_b to end


# 5. Compile the graph
graph = builder.compile()

# Generates the graph as PNG
# graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

# Get result

"""
The invoke function needs the state, in this example we need to follow the
State(TypedDict) signature, in other words, we need a `nodes_path: list[str]`
as the type of state the the invoke function needs.

You can use the class State, created before or you can pass the dictionary
following the `nodes_path: list[str]` signature.
"""
# response = graph.invoke("Send message") # Wrong

"""
This invoke method pass the state (`"nodes_path": []` in this case) to the
other nodes of the graph.
"""
response = graph.invoke({"nodes_path": []})  # this could be the State class

# Result after the graph is all built
print()
print(f"{response=}")
print()
