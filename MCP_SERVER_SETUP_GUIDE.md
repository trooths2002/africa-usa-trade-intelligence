# MCP SERVER DEVELOPMENT GUIDE
## Trade Automation for Free World Trade Inc.

### Quick Start: Trade Data MCP Server

#### 1. Installation Requirements
```bash
# Install Python MCP SDK
pip install mcp

# Install required dependencies
pip install requests pandas python-dotenv
```

#### 2. Basic Trade Data MCP Server (trade_data_server.py)

```python
#!/usr/bin/env python3
"""
Trade Data MCP Server for Free World Trade Inc.
Provides real-time access to trade statistics, AGOA data, and market intelligence.
"""

import asyncio
import json
import os
from typing import Any, Sequence
import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent
)

# Server instance
server = Server("trade-data-server")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available trade data tools."""
    return [
        Tool(
            name="get_agoa_countries",
            description="Get list of AGOA-eligible countries for specified year",
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "string",
                        "description": "Year to check AGOA eligibility (e.g., '2024')"
                    }
                },
                "required": ["year"]
            }
        ),
        Tool(
            name="get_trade_data",
            description="Get US import/export trade data for specific products and countries",
            inputSchema={
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Country name or code"
                    },
                    "product_code": {
                        "type": "string",
                        "description": "HS product code (2, 4, or 6 digits)"
                    },
                    "year": {
                        "type": "string",
                        "description": "Year for trade data"
                    }
                },
                "required": ["country", "product_code", "year"]
            }
        ),
        Tool(
            name="get_product_prices",
            description="Get current commodity prices for agricultural products",
            inputSchema={
                "type": "object",
                "properties": {
                    "commodity": {
                        "type": "string",
                        "description": "Commodity name (e.g., 'coffee', 'cocoa', 'tea')"
                    }
                },
                "required": ["commodity"]
            }
        ),
        Tool(
            name="check_agoa_eligibility",
            description="Check if a specific product from a country is AGOA-eligible",
            inputSchema={
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "African country name"
                    },
                    "product_code": {
                        "type": "string",
                        "description": "HS product code"
                    }
                },
                "required": ["country", "product_code"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for trade data operations."""
    
    if name == "get_agoa_countries":
        year = arguments.get("year", "2024")
        
        # AGOA-eligible countries as of 2024
        agoa_countries = {
            "2024": [
                "Angola", "Benin", "Botswana", "Burkina Faso", "Cameroon",
                "Cape Verde", "Chad", "Comoros", "Democratic Republic of Congo",
                "Republic of Congo", "Côte d'Ivoire", "Djibouti", "Eswatini",
                "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau",
                "Kenya", "Lesotho", "Liberia", "Madagascar", "Malawi", "Mali",
                "Mauritania", "Mauritius", "Mozambique", "Namibia", "Niger",
                "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal",
                "Seychelles", "Sierra Leone", "South Africa", "Tanzania",
                "Togo", "Uganda", "Zambia"
            ]
        }
        
        countries = agoa_countries.get(year, [])
        result = {
            "year": year,
            "total_countries": len(countries),
            "countries": countries,
            "notes": f"AGOA-eligible countries for {year}. Total: {len(countries)} countries."
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_trade_data":
        country = arguments.get("country")
        product_code = arguments.get("product_code")
        year = arguments.get("year")
        
        # Mock trade data - in production, connect to actual APIs
        mock_data = {
            "country": country,
            "product_code": product_code,
            "year": year,
            "import_value_usd": 1250000,
            "export_value_usd": 850000,
            "trade_balance": -400000,
            "top_products": [
                {"description": "Coffee beans", "value": 500000},
                {"description": "Cocoa beans", "value": 300000},
                {"description": "Spices", "value": 200000}
            ],
            "data_source": "US Census Bureau (simulated)",
            "note": "This is simulated data. Connect to actual APIs for production use."
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(mock_data, indent=2)
        )]
    
    elif name == "get_product_prices":
        commodity = arguments.get("commodity").lower()
        
        # Mock commodity prices - connect to World Bank, Bloomberg, etc.
        prices = {
            "coffee": {"price": 1.85, "unit": "USD/lb", "change_pct": 2.3},
            "cocoa": {"price": 2.95, "unit": "USD/lb", "change_pct": -1.2},
            "tea": {"price": 3.20, "unit": "USD/kg", "change_pct": 0.8},
            "cashews": {"price": 4.50, "unit": "USD/lb", "change_pct": 1.5},
            "vanilla": {"price": 285.00, "unit": "USD/kg", "change_pct": -3.2}
        }
        
        result = prices.get(commodity, {"error": f"Price data not available for {commodity}"})
        result["commodity"] = commodity
        result["timestamp"] = "2025-08-30T10:00:00Z"
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "check_agoa_eligibility":
        country = arguments.get("country")
        product_code = arguments.get("product_code")
        
        # Simplified AGOA eligibility check
        agoa_countries = [
            "Angola", "Benin", "Botswana", "Burkina Faso", "Cameroon",
            "Cape Verde", "Chad", "Comoros", "Democratic Republic of Congo",
            "Republic of Congo", "Côte d'Ivoire", "Djibouti", "Eswatini",
            "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau",
            "Kenya", "Lesotho", "Liberia", "Madagascar", "Malawi", "Mali",
            "Mauritania", "Mauritius", "Mozambique", "Namibia", "Niger",
            "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal",
            "Seychelles", "Sierra Leone", "South Africa", "Tanzania",
            "Togo", "Uganda", "Zambia"
        ]
        
        # Simplified product eligibility (real implementation would check detailed HTS codes)
        eligible_products = ["07", "08", "09", "50", "51", "52", "61", "62", "63"]
        product_prefix = product_code[:2]
        
        result = {
            "country": country,
            "product_code": product_code,
            "country_eligible": country in agoa_countries,
            "product_eligible": product_prefix in eligible_products,
            "overall_eligible": country in agoa_countries and product_prefix in eligible_products,
            "note": "This is a simplified check. Consult official AGOA resources for detailed eligibility."
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="trade-data-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
```

#### 3. Configuration File (.env)
```env
# API Keys (add your actual keys)
CENSUS_API_KEY=your_census_api_key_here
WORLD_BANK_API_KEY=your_world_bank_key_here
USDA_API_KEY=your_usda_api_key_here

# Database connections
DATABASE_URL=sqlite:///trade_data.db

# Debug settings
DEBUG=True
LOG_LEVEL=INFO
```

#### 4. Requirements File (requirements.txt)
```txt
mcp>=1.0.0
httpx>=0.25.0
pandas>=2.0.0
python-dotenv>=1.0.0
asyncio-mqtt>=0.16.0
sqlalchemy>=2.0.0
```

#### 5. Installation and Setup

```bash
# Create project directory
mkdir trade-mcp-server
cd trade-mcp-server

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
python trade_data_server.py
```

### Integration with AI Assistant

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "trade-data": {
      "command": "python",
      "args": ["path/to/trade_data_server.py"],
      "env": {
        "CENSUS_API_KEY": "your_key_here"
      }
    }
  }
}
```

### Next Steps

1. **Enhance with Real APIs**:
   - US Census Bureau Trade API
   - World Bank Commodity Price API
   - USDA FAS Export API
   - USTR AGOA Database

2. **Add More Tools**:
   - Shipping rate calculator
   - Currency converter
   - Compliance checker
   - Supplier database

3. **Database Integration**:
   - Store historical data
   - Cache API responses
   - Track performance metrics

### Production Considerations

- **Error Handling**: Add comprehensive error handling and logging
- **Rate Limiting**: Implement API rate limiting and retry logic
- **Security**: Secure API keys and add authentication
- **Monitoring**: Add health checks and performance monitoring
- **Documentation**: Create detailed API documentation

This MCP server will automate much of your trade data research and analysis, saving significant time in your daily operations.