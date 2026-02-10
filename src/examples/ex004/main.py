from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph, add_messages
from rich import print


# 1 - Define state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# 2 - Define nodes
def call_llm(state: AgentState) -> AgentState:
    return state


# 3 - Create StateGraph
builder = StateGraph(
    AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState
)

# 4 - Add nodes to graph
builder.add_node("call_llm", call_llm)

builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

# 5 - Compile graph
graph = builder.compile()

# 6 - Use graph
if __name__ == "__main__":
    result = graph.invoke({"messages": []})
    print(result)
