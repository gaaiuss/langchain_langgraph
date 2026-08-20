import os
from collections.abc import Sequence
from typing import Annotated, TypedDict
from unittest import result

from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.message import Messages
from rich import print
from rich.markdown import Markdown

load_dotenv()

# For now we will create a global llm variable for simplicity purposes
model = os.getenv("MODEL", "Model not found. Check you `.env` file.")
llm = ChatOllama(model=model)


# Just to debug the code
def reducer(a: Messages, b: Messages) -> Messages:
    return add_messages(a, b)


# 1. Define state
class AgentState(TypedDict):  # the state can be any name
    # As a pattern, when you talk about messages history, we call this var
    # messages
    # Every time that you manipulate this field in anywhere of the graph
    # yoy are triggering the reducer that joins the nodes returns to pass it to
    # the next node.
    messages: Annotated[
        # As we do not want the state to be changed directly, we do not want to
        # change the messages directly so we use Sequence for ReadOnly.
        Sequence[BaseMessage],
        reducer,  # our reducer just to trace the triggers
        # add_messages,  # add_messages: reducer from langgraph
    ]


# 2. Create nodes
def call_llm(state: AgentState) -> AgentState:  # this is a node
    # Here we manipulate the 'messages' field of the state, triggering the reducer
    # returning a new state
    # return {"messages": [AIMessage("Hello, how are you?")]}

    # When calling the llm passing a message is not ideal.
    # llm_result = llm.invoke('llm message')

    # Here we will pass
    # ALL the messages for it to have all the history.
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}

    # Simulating a llm result
    # llm_result = AIMessage("Hello, how are you?")
    # return {"messages": [llm_result]}


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
builder.add_node(
    # the name here can be anything but we maintain like this to make the
    # understanding easier
    "call_llm",
    call_llm,
)

# 5. Add edges
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)


# 6. Compile graph
graph = builder.compile()


# 7. Use graph
# if __name__ == "__main__":
#     user_input = "Hello, my name is Caio."
#     human_message = HumanMessage(user_input)
#     result = graph.invoke(
#         # state var messages with a Sequence like a list
#         {"messages": [human_message]},
#     )
#     # get the last message, in this case from the llm
#     print(result["messages"][-1].content)

#     print(Markdown("---"))

#     """
#     Every time the `invoke()` method is called, a new graph is created, that
#     is why the llm do not remember the previous messages.
#     """
#     user_input = "Do you remember my name?"
#     human_message = HumanMessage(user_input)
#     result = graph.invoke(  # this will init a new graph
#         {"messages": [human_message]},
#     )
#     # get the last message, in this case from the llm
#     print(result["messages"][-1].content)

#     print(Markdown("---"))

# Making an infinite loop
if __name__ == "__main__":
    # 1. Creating a variable to store the messages history
    message_history: Sequence[BaseMessage] = []

    while True:
        user_input = input("Type your message: ")
        print(Markdown("---"))

        if user_input.lower() in ["q", "quit"]:
            print("Bye!")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)

        # 2. Unpacking the messages stored from 'step 4.' in history and adding
        # the new human message
        message_history = [*message_history, human_message]

        result = graph.invoke(
            # 3. Now we can pass the message history + human message. Note that
            # this will resend all the tokens everytime you invoke the messages
            # with the message history
            {"messages": message_history},
        )
        # 4. Saving the current messages in the history
        message_history = result["messages"]

        # get the last message, in this case from the llm
        print(Markdown(str(result["messages"][-1].content)))

        print(Markdown("---"))
