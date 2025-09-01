#!/usr/bin/env python3
"""
HTTP API wrapper for MCP Intelligence Server
Provides REST endpoints and health checks for the MCP server
"""

import asyncio
import json
import os
import sys
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add the current directory to the path to help with imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the MCP server
try:
    from server import server, MCP_AVAILABLE, handle_call_tool, handle_list_tools
    HAS_MCP_SERVER = True
except ImportError:
    HAS_MCP_SERVER = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Africa-USA Trade Intelligence API",
    description="REST API for the MCP Intelligence Server",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mcp_available": HAS_MCP_SERVER,
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Africa-USA Trade Intelligence API",
        "status": "running",
        "mcp_server": "available" if HAS_MCP_SERVER else "not_available",
        "endpoints": ["/health", "/tools", "/market_analysis", "/sse/ping"]
    }

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    if not HAS_MCP_SERVER:
        return {"error": "MCP server not available", "tools": []}
    
    try:
        # This would normally call the MCP server's list_tools
        tools = [
            {
                "name": "analyze_market_trends",
                "description": "Analyze current market trends for African agricultural products"
            },
            {
                "name": "find_arbitrage_opportunities", 
                "description": "Find price arbitrage opportunities between Africa and USA"
            },
            {
                "name": "research_suppliers",
                "description": "Research and qualify agricultural suppliers in Africa"
            },
            {
                "name": "analyze_buyer_intelligence",
                "description": "Analyze buyer patterns and preferences in USA markets"
            }
        ]
        return {"tools": tools}
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market_analysis")
async def market_analysis():
    """Get current market analysis"""
    try:
        # Simulate market analysis data
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "overview_kpis": {
                "active_opportunities": 12,
                "monthly_revenue_potential": 850000,
                "commission_potential": 127500,
                "active_suppliers": 34,
                "active_buyers": 28,
                "conversion_rate": 23.5
            },
            "live_opportunities": [
                {
                    "id": 1,
                    "product": "Premium Cashews",
                    "origin_country": "Ghana",
                    "destination": "New York, USA",
                    "price_arbitrage": 45.2,
                    "commission_potential": 35000,
                    "urgency": "High",
                    "agoa_eligible": True,
                    "contact_supplier": "Kwame Enterprises Ltd.",
                    "contact_buyer": "Atlantic Nuts Trading Co.",
                    "last_updated": datetime.now().isoformat()
                }
            ],
            "market_trends": {
                "top_products": ["Cashews", "Coffee", "Shea Butter", "Vanilla", "Spices"],
                "growth_rates": [12.5, 18.3, 15.7, 22.1, 9.8],
                "market_size": [450000, 680000, 320000, 180000, 240000]
            }
        }
        return analysis
    except Exception as e:
        logger.error(f"Error in market analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sse/ping")
async def sse_ping():
    """Server-sent events ping endpoint"""
    def event_stream():
        yield f"data: {json.dumps({'status': 'ping', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"}
    )

@app.get("/sse/market_data")
async def sse_market_data():
    """Server-sent events for market data"""
    def event_stream():
        # Send initial data
        data = {
            "type": "market_update",
            "timestamp": datetime.now().isoformat(),
            "opportunities_count": 12,
            "revenue_potential": 850000
        }
        yield f"data: {json.dumps(data)}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"}
    )

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, arguments: Dict[str, Any] = None):
    """Call a specific MCP tool"""
    if not HAS_MCP_SERVER:
        return {"error": "MCP server not available"}
    
    try:
        # This would normally call the MCP server's call_tool function
        if tool_name == "analyze_market_trends":
            result = {
                "result": "Market analysis complete",
                "trends": ["Growing demand for organic products", "AGOA benefits driving growth"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            result = {
                "result": f"Tool {tool_name} executed",
                "timestamp": datetime.now().isoformat()
            }
        
        return result
    except Exception as e:
        logger.error(f"Error calling tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Main entry point for the HTTP API server"""
    port = int(os.getenv('MCP_SERVER_PORT', '8000'))
    host = os.getenv('MCP_SERVER_HOST', '0.0.0.0')
    
    logger.info(f"Starting Africa-USA Trade Intelligence API on {host}:{port}")
    logger.info(f"MCP Server Available: {HAS_MCP_SERVER}")
    
    uvicorn.run(
        "api_wrapper:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()