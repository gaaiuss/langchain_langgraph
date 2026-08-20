"""Checkpointer

For the purpose of not needing to save the context history hardcoded we use the
checkpointer feature.

For each interaction with the state, the checkpointer saves it in memory, a
database, etc to send the context history to the AI.

To start using the checkpointer you will need a thread id, a number to store
the context history the is configured inside the graph invoke or creation.
"""

import os
import threading
from collections.abc import Sequence
from typing import Annotated, TypedDict
from unittest import result

from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.markdown import Markdown

load_dotenv()

# For now we will create a global llm variable for simplicity purposes
model = os.getenv("MODEL", "Model not found. Check you `.env` file.")
llm = ChatOllama(model=model)


# 1. Define state
class AgentState(TypedDict):
    messages: Annotated[
        Sequence[BaseMessage],
        add_messages,  # add_messages: reducer from langgraph
    ]


# 2. Create nodes
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}


# 3. Create the StateGraph or builder
builder = StateGraph(
    AgentState,
    # Just listing what comes by default for we are going to detail this further
    # in the future
    context_schema=None,
    input_schema=AgentState,
    output_schema=AgentState,
)


# 4. Add nodes to the graph
builder.add_node("call_llm", call_llm)

# 5. Add edges
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

# Creating the checkpointer
checkpointer = InMemorySaver()

# Creating the config that the checkpointer needs
# config = RunnableConfig(configurable={"thread_id": 1})  # This number can be any.

# You can also get the id dinamically using threading
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

# 6. Compile graph
graph = builder.compile(checkpointer=checkpointer)


# 7. Use graph
if __name__ == "__main__":
    while True:
        user_input = input("Type your message: ")
        print(Markdown("---"))

        if user_input.lower() in ["q", "quit"]:
            print("Bye!")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke(
            {"messages": [human_message]},
            # Here we are configuring the thread id that will be used by the
            # checkpointer to store the message history.
            config=config,
        )

        # get the last message, in this case from the llm
        print(Markdown(str(result["messages"][-1].content)))
        print(Markdown("---"))
