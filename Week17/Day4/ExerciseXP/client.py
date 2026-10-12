# client.py - spawns server.py over STDIO, discovers its features and invokes them
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="mcp", args=["run", "server.py"], env=None
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f"Connected to server: {init.serverInfo.name} (protocol {init.protocolVersion})")

            # List resources: concrete resources and URI templates such as greeting://{name}
            resources = await session.list_resources()
            templates = await session.list_resource_templates()
            print("Resources:", [str(r.uri) for r in resources.resources] or "(no static resources)")
            print("Resource templates:", [t.uriTemplate for t in templates.resourceTemplates])

            # List tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])
            for t in tools.tools:
                print(f"  - {t.name}: {t.description} | input schema: {t.inputSchema}")

            # Read greeting://hello
            content = await session.read_resource("greeting://hello")
            print("greeting://hello ->", content.contents[0].text)

            # Call the add tool with a=1, b=7
            result = await session.call_tool("add", arguments={"a": 1, "b": 7})
            print("add(1, 7) ->", result.content[0].text,
                  "| structured:", getattr(result, "structuredContent", None))


if __name__ == "__main__":
    asyncio.run(run())
