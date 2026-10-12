# server.py - minimal MCP weather server (no LLM): one tool + one resource over STDIO
import logging
import sys

from mcp.server.fastmcp import FastMCP

# Log to stderr: on the STDIO transport, stdout is reserved for JSON-RPC messages.
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="[server] %(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("weather")

mcp = FastMCP("WeatherDemo")

# Small static, in-memory "database"
WEATHER = {
    "Paris": {"temp_c": 21, "condition": "sunny", "humidity_pct": 48},
    "London": {"temp_c": 15, "condition": "cloudy", "humidity_pct": 72},
    "NYC": {"temp_c": 26, "condition": "humid", "humidity_pct": 80},
    "Tel Aviv": {"temp_c": 30, "condition": "clear", "humidity_pct": 60},
}


@mcp.tool()
def get_weather(city: str) -> dict:
    """Return static weather data for a supported city (see the cities://list resource)."""
    log.info("get_weather called with city=%r", city)
    match = next((c for c in WEATHER if c.lower() == city.strip().lower()), None)
    if match is None:
        log.warning("unknown city %r", city)
        return {"error": f"City '{city}' not supported", "supported": list(WEATHER)}
    return {"city": match, **WEATHER[match]}


@mcp.resource("cities://list")
def list_cities() -> str:
    """Newline-separated list of the supported cities."""
    log.info("cities://list read")
    return "\n".join(WEATHER)


if __name__ == "__main__":
    log.info("WeatherDemo server starting on STDIO")
    mcp.run()  # default transport: stdio
