# MCP Servers Connection Guide

This guide explains how to connect and use all the MCP servers configured in your system.

## Overview of Configured MCP Servers

Your [mcp.json](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/mcp.json) configuration includes the following MCP servers:

1. **newsIntelligence** - HTTP server for news intelligence
2. **newsIntelligenceStdio** - STDIO server for news intelligence
3. **marketIntelligence** - HTTP server for market intelligence (SSE)
4. **memory** - Memory storage server
5. **sequentialthinking** - Sequential thinking processing server
6. **github** - GitHub Copilot integration
7. **context7** - Upstash Context7 integration
8. **huggingface** - Hugging Face integration
9. **codacy** - Codacy integration
10. **azure-devops** - Azure DevOps integration
11. **africaTradeIntelligence** - Africa-USA trade intelligence server (STDIO)

## Prerequisites

Before connecting to these servers, ensure you have:

1. Python 3.9+ installed
2. Node.js installed (for npx-based servers)
3. Required Python packages installed:
   ```bash
   pip install -r requirements.txt
   ```

## Server Connection Details

### 1. Africa Trade Intelligence Server (africaTradeIntelligence)

This is your custom MCP server for Africa-USA agricultural trade intelligence.

- **Type**: STDIO
- **Command**: `python src/mcp_servers/market_intelligence/server.py`
- **Features**:
  - Real-time arbitrage detection
  - Market intelligence gathering
  - Supplier and buyer intelligence
  - Automated data collection

To test this server specifically:
```bash
python src/mcp_servers/market_intelligence/server.py
```

### 2. Memory Server (memory)

- **Type**: STDIO
- **Command**: `npx -y @modelcontextprotocol/server-memory`
- **Environment**: Requires `MEMORY_FILE_PATH` input

### 3. Sequential Thinking Server (sequentialthinking)

- **Type**: STDIO
- **Command**: `npx -y @modelcontextprotocol/server-sequential-thinking`

### 4. GitHub Copilot Server (github)

- **Type**: HTTP
- **URL**: `https://api.githubcopilot.com/mcp/`

### 5. Context7 Server (context7)

- **Type**: STDIO
- **Command**: `npx -y @upstash/context7-mcp@latest`

### 6. Hugging Face Server (huggingface)

- **Type**: HTTP
- **URL**: `https://hf.co/mcp`

### 7. Codacy Server (codacy)

- **Type**: STDIO
- **Command**: `npx -y @codacy/codacy-mcp`
- **Environment**: Requires `CODACY_ACCOUNT_TOKEN` input

### 8. Azure DevOps Server (azure-devops)

- **Type**: STDIO
- **Command**: `npx -y @azure-devops/mcp ${input:ado_org}`

## Testing Server Connections

### Automated Testing

Run the automated test script to verify all server connections:

```bash
# Using the batch file (Windows)
test_mcp_connections.bat

# Or directly with Python
python scripts/test_all_mcp_servers.py
```

### Manual Testing

To manually test any STDIO server:

```bash
# For your Africa Trade Intelligence server
python src/mcp_servers/market_intelligence/server.py

# For npx-based servers
npx -y @modelcontextprotocol/server-memory
```

For HTTP servers, you can test connectivity using curl:

```bash
# Test if the server responds
curl -v http://127.0.0.1:6010/sse
```

## Using the Servers with an MCP Client

To use these servers with an MCP client:

1. Ensure all required dependencies are installed
2. Start your MCP client application
3. The client should automatically discover and connect to all configured servers
4. You can then use the tools provided by each server

### Example Client Integration

If you're building an MCP client, you would typically:

```python
# Example pseudo-code for an MCP client
import mcp.client

# Load configuration
config = load_mcp_config('mcp.json')

# Initialize client with all servers
client = mcp.client.Client(config)

# List available tools from all servers
tools = client.list_tools()

# Call a specific tool
result = client.call_tool('scan_arbitrage_opportunities', {
    'min_margin': 20,
    'countries': ['ET', 'KE', 'GH']
})
```

## Troubleshooting Common Issues

### 1. Server Not Found Errors

- Ensure all required dependencies are installed
- Check that file paths in the configuration are correct
- Verify that Python and Node.js are properly installed

### 2. Permission Errors

- Run your terminal as Administrator on Windows
- Ensure you have read/write permissions to the project directory

### 3. Port Conflicts

- For HTTP servers, ensure the specified ports are available
- Check if other services are using the same ports

### 4. Authentication Issues

- For servers requiring tokens (Codacy, Azure DevOps), ensure you've provided the required inputs
- Check that your tokens are valid and have the necessary permissions

## Next Steps

1. Run the automated test script to verify all connections
2. Start developing applications that utilize these MCP servers
3. Extend the configuration with additional servers as needed
4. Monitor server performance and logs for any issues

## Additional Resources

- [MCP_SERVER_SETUP_GUIDE.md](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/MCP_SERVER_SETUP_GUIDE.md) - Detailed setup instructions
- [src/mcp_servers/market_intelligence/server.py](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/src/mcp_servers/market_intelligence/server.py) - Custom Africa trade intelligence server implementation
- [test_mcp_server.py](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/test_mcp_server.py) - Test scripts for MCP functionality