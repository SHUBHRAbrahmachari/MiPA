from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
import json


async def load_tools() -> list[BaseTool]:
    with open("config.json", "r") as f:
        config = json.load(f)

    MCP_SERVERS = config.get("mcp_servers")

    try:
        client = MultiServerMCPClient(MCP_SERVERS)
        return await client.get_tools()

    except Exception as e:
        print("SOMETHING WENT WRONG WHILE TRYING TO CONNECT WITH MCP SERVERS(S)")
        print(str(e))
        return []
