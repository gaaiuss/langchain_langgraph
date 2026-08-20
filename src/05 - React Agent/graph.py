from typing import Literal

from langchain.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import ValidationError
from state import State
from tools import TOOLS, TOOLS_BY_NAME
from utils import load_ollama


def call_llm(state: State) -> State:
    print("> call_llm")
    llm_with_tools = load_ollama().bind_tools(TOOLS)
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": [result]}


def tool_node(state: State) -> State:
    print("> tool node")
    llm_response = state["messages"][-1]

    if not isinstance(llm_response, AIMessage) or not getattr(
        llm_response,
        "tool_calls",
        None,
    ):
        return state

    last_tool_call = llm_response.tool_calls[-1]
    name, args, id_ = (
        last_tool_call["name"],
        last_tool_call["args"],
        last_tool_call["id"],
    )

    try:
        content = TOOLS_BY_NAME[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError) as error:
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)

    return {"messages": [tool_message]}


def router(state: State) -> Literal["tool_node", "__end__"]:
    print("> router")
    llm_response = state["messages"][-1]

    if getattr(llm_response, "tool_calls", None):
        return "tool_node"
    return "__end__"


def build_graph() -> CompiledStateGraph[State, None, State, State]:
    builder = StateGraph(State)

    builder.add_node("call_llm", call_llm)
    builder.add_node("tool_node", tool_node)

    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges("call_llm", router, ["tool_node", "__end__"])
    builder.add_edge("tool_node", "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
