"""LLM with Tools

By using the @tool decoration we can give the llm access to a python function
and use it in the response.

You have to detail very well the function for the llm to understand how to use
it.

Just to make clear, the LLM does not use the tool directly, from the moment
that it assumes that it will use a tool after the user asked, the llm asks for
the dev to use that tool. After running the tool, the dev injects the tool
return bak to the llm.
"""

import os

from dotenv import load_dotenv
from langchain.tools import BaseTool, tool
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_ollama import ChatOllama
from pydantic import ValidationError
from rich import print
from rich.markdown import Markdown


# 1. Creating tools
@tool
def multiply(a: float, b: float) -> float:
    # This is just an example of a function docstring for the llm to
    # unsderstand exactly how and when to use this tool
    """Multiply a * b and returns the result

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        the resulting float of the equation a * b
    """
    return a * b


print(Markdown("---"))

# # If we should use the tool we use the invoke method
# result = multiply.invoke({"a": 5.2, "b": 10})
# print(result)

load_dotenv()
model = os.getenv("MODEL", "Model not found. Check you `.env` file.")
llm = ChatOllama(model=model)

system_message = SystemMessage(
    "You are an assistant. You have access to tools. When the user asks "
    "for something, first look if you have a tool that solves that problem.",
)
human_message = HumanMessage(
    "Hi my name is Caio. Can you tell me how much is 52.2 times 10?",
)
messages: list[BaseMessage] = [system_message, human_message]


tool_belt: list[BaseTool] = [multiply]  # add your tools here

# Right here we are associating or mapping each too a name to call it later on
tools_by_name = {tool.name: tool for tool in tool_belt}

# This is a new llm binded with tools
llm_with_tools = llm.bind_tools(tool_belt)

llm_response = llm_with_tools.invoke(messages)
messages.append(llm_response)

# First we need to check if the llm_response have the tool_calls key to check
# if we will need to call a tool for it to resolve a task
if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls", None):
    # For this case we need only the last call
    last_call = llm_response.tool_calls[-1]

    # Here we are unpacking the attrs we will use from the call inside the tool
    # call
    name, args, id_ = last_call["name"], last_call["args"], last_call["id"]

    # As we are not shure that the call will have a correct name we will try
    # to get it and handle the exceptions
    try:
        # Here we are invoking the tool using the tool name as
        # 'tools_by_name[name]'
        content = tools_by_name[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError) as error:
        # assuming that it made a mistake we send the error back to the llm for
        # it to fix it by itself
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    # Appending the tool response to the messages
    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    messages.append(tool_message)

    # Giving the tool response back to the llm and adding it to the history
    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)

    print(messages)  # Printing the message history

print(Markdown("---"))
