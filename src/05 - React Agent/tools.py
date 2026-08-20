from langchain.tools import tool


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


@tool
def divide(a: float, b: float) -> float:
    """Divide a / b and returns the result

    Args:
        a: float dividend
        b: float divider

    Returns:
        the resulting float of the equation a / b
    """
    return a / b


@tool
def sum_(a: float, b: float) -> float:
    """Sum a + b and returns the result

    Args:
        a: float
        b: float

    Returns:
        the resulting float of the equation a + b
    """
    return a + b


@tool
def sub_(a: float, b: float) -> float:
    """Subtracts a - b and returns the result

    Args:
        a: float
        b: float

    Returns:
        the resulting float of the equation a - b
    """
    return a - b
