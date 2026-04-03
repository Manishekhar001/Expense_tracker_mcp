import json
import random

from fastmcp import FastMCP

mcp = FastMCP("Simple Claculator Server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together
    Args :
        a : first number
        b : Second number

    Returns :
        The sum of a and b
    """
    return a + b


@mcp.tool
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random number within a range.
    Args :
        min_val : Minimum value (default: 1)
        max_val : Maximum value (default: 100)

    Return :
        A random number between min_val and max_val
    """

    return random.randint(min_val, max_val)


@mcp.resource("info://server")
def server_info() -> str:
    """Get the information about this server"""
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A bsic MCP server with math tools.",
        "tools": ["add", "random_number"],
        "author": "Mani",
    }
    return json.dumps(info, indent=2)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
