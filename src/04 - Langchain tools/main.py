"""LLM Tools

By using the @tool decoration we can give the llm access to a python function
and use it in the response.

You have to detail very well the function for the llm to understand how to use
it.
"""

from langchain.tools import tool


# 1. Creating tools
@tool
def multiply(a: float, b: float) -> float:
    """Multiply a * b and returns the result

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        the resulting float of the equation a * b
    """
    return a * b
