#!/usr/bin/env python3
"""
Async tests for the real MCP stdio server using the official mcp client SDK.
"""
import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional

import pytest

from mcp import ClientSession, StdioServerParameters  # type: ignore
from mcp.client.stdio import stdio_client  # type: ignore


def _get_text_from_content_item(item: Any) -> Optional[str]:
    # Support both typed objects and dicts
    if hasattr(item, "text"):
        return getattr(item, "text")
    if isinstance(item, dict):
        return item.get("text")
    return None


def _extract_tools(list_tools_result: Any) -> List[Any]:
    if list_tools_result is None:
        return []
    if isinstance(list_tools_result, dict):
        return list_tools_result.get("tools", [])
    if hasattr(list_tools_result, "tools"):
        return getattr(list_tools_result, "tools")
    return []


@pytest.mark.asyncio
async def test_mcp_server_list_and_call_tools():
    # Use the current Python interpreter to launch the server script
    command = sys.executable
    server_script = os.path.join("src", "mcp", "market_intelligence_server.py")

    server_params = StdioServerParameters(
        command=command,
        args=[server_script],
        env={},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session (API signature may vary by mcp version)
            try:
                await session.initialize("tests-mcp-client")
            except TypeError:
                # Fallback for versions where initialize() takes no arguments
                await session.initialize()

            # List tools and validate expected names exist
            list_result = await session.list_tools()
            tools = _extract_tools(list_result)
            names = []
            for t in tools:
                name = getattr(t, "name", None)
                if name is None and isinstance(t, dict):
                    name = t.get("name")
                names.append(name)

            assert "discover_optimal_tech_stack" in names
            assert "scan_arbitrage_opportunities" in names
            assert "analyze_market_trends" in names
            assert "generate_expert_content" in names

            # Call a tool and verify we get text JSON content back
            call_result = await session.call_tool(
                "discover_optimal_tech_stack",
                {"budget": "free", "requirements": ["fast", "reliable"]},
            )

            # call_result may expose a .content attribute or be a dict
            if hasattr(call_result, "content"):
                content_list = call_result.content
            elif isinstance(call_result, dict):
                content_list = call_result.get("content", [])
            else:
                content_list = []

            assert content_list, "Expected non-empty content from tool call"
            text = _get_text_from_content_item(content_list[0])
            assert text is not None

            # Ensure returned text is valid JSON with expected key
            data = json.loads(text)
            assert "recommended_stack" in data

