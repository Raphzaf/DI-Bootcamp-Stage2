import logging, sys
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="[server] %(message)s")   # never log to stdout on STDIO
mcp = FastMCP("CalcDemo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers a and b and return the sum."""
    logging.info("add(%s, %s)", a, b)
    return a + b


@mcp.resource("info://about")
def about() -> str:
    """Short description of this server."""
    return "CalcDemo MCP server: exposes arithmetic tools for LLM agents."


if __name__ == "__main__":
    mcp.run()


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers a and b and return the product."""
    logging.info("multiply(%s, %s)", a, b)
    return a * b
