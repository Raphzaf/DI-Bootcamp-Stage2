# server.py - a tiny MCP server exposing one tool and one resource over STDIO
from mcp.server.fastmcp import FastMCP

# Create an MCP server with a name
mcp = FastMCP("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    """Return a personalised greeting (read-only context)."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Start the server loop on STDIO (default transport)
    mcp.run(transport="stdio")
