# MCP Client Guide

This guide explains how to use the [mcp.json](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/mcp.json) configuration file to create an MCP client that can connect to all the defined servers.

## Overview

The [mcp.json](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/mcp.json) file defines 11 MCP servers that can be connected to:

1. **newsIntelligence** (HTTP)
2. **newsIntelligenceStdio** (STDIO)
3. **marketIntelligence** (HTTP)
4. **memory** (STDIO)
5. **sequentialthinking** (STDIO)
6. **github** (HTTP)
7. **context7** (STDIO)
8. **huggingface** (HTTP)
9. **codacy** (STDIO)
10. **azure-devops** (STDIO)
11. **africaTradeIntelligence** (STDIO)

## Using the Configuration File

To use the configuration file in a Python client, you would:

1. Load the JSON configuration
2. Parse the server definitions
3. Create connections to each server based on their type (HTTP or STDIO)

## Example Client Implementation

Here's a simplified example of how to create a client that uses the configuration:

```python
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import httpx

class MCPClientFromConfig:
    def __init__(self, config_path: str = "mcp.json"):
        """Initialize client with configuration file"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.sessions = {}
    
    async def connect_stdio_server(self, name: str, config: dict):
        """Connect to a STDIO server"""
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config.get("env", {})
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize(f"client-for-{name}")
                    self.sessions[name] = session
                    print(f"✅ Connected to {name}")
                    return session
        except Exception as e:
            print(f"❌ Failed to connect to {name}: {e}")
            return None
    
    async def connect_http_server(self, name: str, config: dict):
        """Connect to an HTTP server (simplified)"""
        url = config["url"]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ HTTP server {name} is reachable")
                    return True
                else:
                    print(f"❌ HTTP server {name} returned {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Failed to connect to HTTP server {name}: {e}")
            return False
    
    async def connect_all_servers(self):
        """Connect to all servers defined in configuration"""
        for name, config in self.config["servers"].items():
            server_type = config["type"]
            
            if server_type == "stdio":
                await self.connect_stdio_server(name, config)
            elif server_type == "http":
                await self.connect_http_server(name, config)
    
    async def list_all_tools(self):
        """List tools from all connected STDIO servers"""
        for name, session in self.sessions.items():
            try:
                tools = await session.list_tools()
                print(f"\nTools from {name}:")
                if tools and hasattr(tools, 'tools'):
                    for tool in tools.tools:
                        print(f"  • {tool.name}: {tool.description}")
            except Exception as e:
                print(f"  ❌ Error listing tools from {name}: {e}")

# Usage example
async def main():
    client = MCPClientFromConfig("mcp.json")
    await client.connect_all_servers()
    await client.list_all_tools()

# Run the client
# asyncio.run(main())
```

## Client Scripts in This Repository

This repository includes several client scripts:

1. **[scripts/mcp_python_client.py](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/scripts/mcp_python_client.py)** - A comprehensive client that attempts to connect to all servers
2. **[scripts/simple_mcp_client.py](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/scripts/simple_mcp_client.py)** - A focused client for the Africa Trade Intelligence server
3. **[test_simple_server.py](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/test_simple_server.py)** - A test client for the simple server implementation

## Running the Clients

### Using the Batch Files (Windows)

```bash
# Run the comprehensive client
run_mcp_client.bat

# Run the simple client
run_simple_mcp_client.bat
```

### Direct Execution

```bash
# Run the comprehensive client
python scripts/mcp_python_client.py

# Run the simple client
python scripts/simple_mcp_client.py

# Test the simple server
python test_simple_server.py
```

## Important Notes

1. **Server Availability**: Not all servers may be available or running. HTTP servers need to be actively running on their specified ports, and STDIO servers need to have their commands available in your system PATH.

2. **Dependencies**: Make sure all required dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Authentication**: Some servers (like GitHub, Codacy) may require authentication tokens that need to be provided as environment variables or inputs.

4. **Error Handling**: The client implementations include error handling for common connection issues, but you may need to adjust them based on your specific environment.

## Customizing the Client

You can extend the client to:

1. Add new server types
2. Implement more sophisticated error handling
3. Add logging and monitoring
4. Create specific workflows that use multiple servers
5. Add caching for tool responses

## Troubleshooting

### Connection Issues

1. **Check that server commands are available**:
   ```bash
   # For STDIO servers, check if commands exist
   which python
   which npx
   which node
   ```

2. **Verify HTTP servers are running**:
   ```bash
   # Check if ports are open
   netstat -an | findstr :3006
   netstat -an | findstr :6010
   ```

3. **Check firewall settings** that might block connections

### Authentication Issues

1. **Ensure environment variables are set** for servers that require authentication
2. **Check that tokens are valid** and have the required permissions

## Additional Resources

- [MCP_SERVERS_FINAL_SUMMARY.md](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/MCP_SERVERS_FINAL_SUMMARY.md) - Final configuration summary
- [MCP_PYTHON_CLIENT_GUIDE.md](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/MCP_PYTHON_CLIENT_GUIDE.md) - Detailed client guide
- [src/mcp_servers/market_intelligence/server.py](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/src/mcp_servers/market_intelligence/server.py) - Custom Africa trade intelligence server implementation