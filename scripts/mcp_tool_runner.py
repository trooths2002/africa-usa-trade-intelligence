#!/usr/bin/env python3
"""
CLI tool runner for the MCP stdio server.
Usage examples:
  python scripts/mcp_tool_runner.py list-tools
  python scripts/mcp_tool_runner.py call-tool analyze_market_trends --args '{"timeframe":"monthly","products":["coffee","cocoa"]}'
"""
import argparse
import asyncio
import json
import os
import sys
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters  # type: ignore
from mcp.client.stdio import stdio_client  # type: ignore


async def run():
    parser = argparse.ArgumentParser(description="MCP Tool Runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-tools", help="List all available MCP tools")

    call = sub.add_parser("call-tool", help="Call a specific tool by name")
    call.add_argument("tool_name", help="Name of the tool to call")
    call.add_argument("--args", default="{}", help="JSON arguments for the tool")

    args = parser.parse_args()

    # Launch server via stdio
    command = sys.executable
    server_script = os.path.join("src", "mcp", "market_intelligence_server.py")
    server_params = StdioServerParameters(command=command, args=[server_script], env={})

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session (handle SDK variant signatures)
            try:
                await session.initialize("cli-tool-runner")
            except TypeError:
                await session.initialize()

            if args.cmd == "list-tools":
                result = await session.list_tools()
                tools = getattr(result, "tools", result.get("tools", []))
                print(json.dumps([
                    {"name": getattr(t, "name", getattr(t, "title", None) or getattr(t, "id", None) or getattr(t, "__dict__", {}).get("name")),
                     "description": getattr(t, "description", None)}
                    for t in tools
                ], indent=2))
            elif args.cmd == "call-tool":
                try:
                    payload: Dict[str, Any] = json.loads(args.args)
                except Exception as e:
                    print(f"Invalid JSON for --args: {e}")
                    sys.exit(1)
                result = await session.call_tool(args.tool_name, payload)
                content = getattr(result, "content", result.get("content", []))
                print(json.dumps([getattr(c, "text", getattr(c, "__dict__", {}).get("text")) for c in content], indent=2))


if __name__ == "__main__":
    asyncio.run(run())

