#!/usr/bin/env python3
"""
Real MCP server for Africa-USA Trade Intelligence tools (STDIO transport).
Implements the Model Context Protocol using the official `mcp` Python SDK.
"""
import asyncio
import json
import os
import sys
from typing import Any, Dict, List

# Ensure the src directory (project root/src) is on sys.path when running as a script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from mcp.server import Server, InitializationOptions  # type: ignore
from mcp.server.stdio import stdio_server  # type: ignore
from mcp.types import Tool, TextContent  # type: ignore

# Project services
from data.collector import DataCollector  # type: ignore
from intelligence.server import IntelligenceServer  # type: ignore

# Create the MCP server and project service instances
server = Server("africa-trade-intelligence")
_data_collector = DataCollector()
_intel = IntelligenceServer(_data_collector)


def _tool(name: str, description: str, input_schema: Dict[str, Any]) -> Tool:
    return Tool(name=name, description=description, inputSchema=input_schema)


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available market intelligence tools."""
    return [
        _tool(
            name="discover_optimal_tech_stack",
            description=(
                "Analyze and recommend the best free technology stack for Africa-USA trade intelligence"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "requirements": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific technical requirements",
                    },
                    "budget": {
                        "type": "string",
                        "description": "Budget constraints (free, minimal, moderate)",
                    },
                },
                "required": ["budget"],
            },
        ),
        _tool(
            name="scan_arbitrage_opportunities",
            description=(
                "Identify high-margin trading opportunities between Africa and USA"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "min_margin": {
                        "type": "number",
                        "description": "Minimum profit margin percentage to consider",
                    },
                    "product_categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Product categories to analyze",
                    },
                    "focus_countries": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "African countries to focus on",
                    },
                },
                "required": ["min_margin"],
            },
        ),
        _tool(
            name="analyze_market_trends",
            description=(
                "Comprehensive market trend analysis for strategic planning"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "timeframe": {
                        "type": "string",
                        "enum": ["weekly", "monthly", "quarterly", "yearly"],
                        "description": "Analysis timeframe",
                    },
                    "products": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Products to analyze",
                    },
                },
                "required": ["timeframe"],
            },
        ),
        _tool(
            name="generate_expert_content",
            description=(
                "Generate expert-level content for social media and thought leadership"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "content_type": {
                        "type": "string",
                        "enum": [
                            "linkedin_post",
                            "twitter_thread",
                            "blog_article",
                            "market_insight",
                        ],
                        "description": "Type of content to generate",
                    },
                    "topic": {
                        "type": "string",
                        "description": "Specific topic or theme",
                    },
                    "target_audience": {
                        "type": "string",
                        "description": "Target audience (buyers, suppliers, general)",
                    },
                },
                "required": ["content_type", "topic"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls by name with JSON arguments."""
    try:
        if name == "discover_optimal_tech_stack":
            budget = arguments.get("budget", "free")
            requirements = arguments.get("requirements", [])
            tech_stack = {
                "analysis_criteria": {
                    "budget_constraint": budget,
                    "requirements": requirements,
                    "optimization_focus": "Maximum ROI with free resources",
                },
                "recommended_stack": {
                    "backend": {
                        "language": "Python 3.10+",
                        "framework": "FastAPI",
                        "database": "SQLite (built-in)",
                        "mcp_server": "Official MCP Python SDK",
                        "rationale": "High performance, free, and mature ecosystem",
                    },
                    "frontend": {
                        "dashboard": "Streamlit",
                        "analytics": "Plotly",
                        "rationale": "Rapid development and rich visuals",
                    },
                    "data_sources": {
                        "trade_data": "US Census Bureau API (Free)",
                        "commodity_prices": "World Bank API (Free)",
                        "currency": "ExchangeRate.host (Free)",
                        "news": "RSS Feeds (Free)",
                    },
                    "automation": {
                        "scheduling": "GitHub Actions + APScheduler",
                        "notifications": "Email/Telegram (free tiers)",
                    },
                },
            }
            return [TextContent(type="text", text=json.dumps(tech_stack, indent=2))]

        elif name == "scan_arbitrage_opportunities":
            min_margin = float(arguments.get("min_margin", 20.0))
            # Use IntelligenceServer to gather opportunities
            intel_data = _intel.get_african_market_intelligence()
            opportunities = intel_data.get("opportunities", [])
            # Attach a simple heuristic for gross_margin text and filter if desired
            enriched = []
            for opp in opportunities:
                opp_copy = dict(opp)
                opp_copy.setdefault("gross_margin", "30-45%")
                enriched.append(opp_copy)
            result = {
                "parameters": {"min_margin": min_margin},
                "high_priority_opportunities": enriched,
                "market_sentiment": intel_data.get("analysis", {}).get("market_sentiment", "neutral"),
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "analyze_market_trends":
            timeframe = arguments.get("timeframe", "monthly")
            products = arguments.get("products", ["coffee", "cocoa", "cashews"])
            intel_data = _intel.get_african_market_intelligence()
            prices = _data_collector.get_commodity_prices().get("prices", {})
            trends = {
                "timeframe": timeframe,
                "products": products,
                "summary": {
                    "overall_market": {
                        "trend": intel_data.get("analysis", {}).get("market_sentiment", "neutral"),
                        "top_commodities": intel_data.get("analysis", {}).get("top_commodities", []),
                    }
                },
                "current_prices": {k: prices.get(k) for k in products if k in prices},
            }
            return [TextContent(type="text", text=json.dumps(trends, indent=2))]

        elif name == "generate_expert_content":
            content_type = arguments.get("content_type")
            topic = arguments.get("topic")
            target = arguments.get("target_audience", "general")
            content = {
                "content_type": content_type,
                "topic": topic,
                "target_audience": target,
                "draft": f"Expert insight on {topic}: key trends, opportunities, and actionable steps for {target}.",
            }
            return [TextContent(type="text", text=json.dumps(content, indent=2))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main() -> None:
    # Run a stdio MCP server
    async with stdio_server() as (read, write):
        # Provide minimal, valid initialization options per MCP spec
        init_opts = InitializationOptions(
            server_name="africa-trade-intelligence",
            server_version="1.0.0",
            capabilities={
                "tools": {},
                # You can extend: 'resources': {}, 'prompts': {}, 'logging': {}, 'completions': {}
            },
            instructions=None,
        )
        await server.run(read, write, initialization_options=init_opts)


if __name__ == "__main__":
    asyncio.run(main())
