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

from typing import TypedDict


# 1. Define node state (TypedDict or dataclass)
class State(TypedDict):
    # for each node executed, it will store the path in a list[str]
    nodes_path: list[str]


# 2. Create the nodes
def node_a(state: State) -> State: ...


def node_b(state: State) -> State: ...
