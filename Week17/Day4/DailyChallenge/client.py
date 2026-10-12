# client.py - spawns the WeatherDemo server over STDIO, discovers and invokes its features
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="mcp", args=["run", "server.py"], env=None)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f"Connected to: {init.serverInfo.name}")

            resources = await session.list_resources()
            print("Resources:", [str(r.uri) for r in resources.resources])

            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])
            for t in tools.tools:
                print(f"  {t.name}: {t.description}  args={list(t.inputSchema['properties'])}")

            cities = await session.read_resource("cities://list")
            print("cities://list ->")
            print(cities.contents[0].text)

            for city in ["Paris", "Berlin"]:  # a valid city and an unsupported one
                result = await session.call_tool("get_weather", arguments={"city": city})
                data = result.structuredContent or json.loads(result.content[0].text)
                print(f"get_weather({city!r}) ->", data)


if __name__ == "__main__":
    asyncio.run(run())
