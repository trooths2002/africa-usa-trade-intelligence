#!/usr/bin/env python3
"""
MCP Python Client
A client that connects to all MCP servers defined in mcp.json
"""

import json
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, config_path: str = "mcp.json"):
        """Initialize the MCP client with configuration file"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.sessions = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load the MCP configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    async def connect_stdio_server(self, name: str, config: Dict[str, Any]) -> Optional[ClientSession]:
        """Connect to a STDIO-based MCP server"""
        command = config.get("command")
        args = config.get("args", [])
        
        if not command:
            raise ValueError(f"No command specified for server {name}")
            
        # Check if the command exists
        try:
            subprocess.run([command, "--help"], capture_output=True, timeout=5)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠️  Command '{command}' may not be available for server {name}")
            return None
            
        try:
            # Create server parameters
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=config.get("env", {})
            )
            
            # Create client session
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize(f"mcp-python-client-{name}")
                    self.sessions[name] = session
                    print(f"✅ Connected to STDIO server: {name}")
                    return session
        except Exception as e:
            print(f"❌ Failed to connect to STDIO server {name}: {e}")
            return None
    
    async def connect_http_server(self, name: str, config: Dict[str, Any]) -> Optional[ClientSession]:
        """Connect to an HTTP-based MCP server"""
        url = config.get("url")
        
        if not url:
            raise ValueError(f"No URL specified for server {name}")
            
        # For HTTP servers, we would typically use a different approach
        # This is a simplified implementation
        try:
            # Test if the server is reachable
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ HTTP server {name} is reachable at {url}")
                    # Note: Full HTTP MCP client implementation would be more complex
                    # This is just a basic connectivity check
                    return None
                else:
                    print(f"❌ HTTP server {name} returned status {response.status_code}")
                    return None
        except Exception as e:
            print(f"❌ Failed to connect to HTTP server {name}: {e}")
            return None
    
    async def connect_all_servers(self) -> None:
        """Connect to all servers defined in the configuration"""
        servers = self.config.get("servers", {})
        
        print("🚀 Connecting to all MCP servers...")
        print("=" * 50)
        
        for name, config in servers.items():
            server_type = config.get("type")
            
            try:
                if server_type == "stdio":
                    await self.connect_stdio_server(name, config)
                elif server_type == "http":
                    await self.connect_http_server(name, config)
                else:
                    print(f"❓ Unknown server type for {name}: {server_type}")
                    continue
                    
            except Exception as e:
                print(f"❌ Failed to connect to {name}: {e}")
                continue
    
    async def list_all_tools(self) -> None:
        """List tools from all connected servers"""
        if not self.sessions:
            print("⚠️  No servers connected. Cannot list tools.")
            return
            
        print("\n🛠️  Available Tools:")
        print("=" * 50)
        
        for name, session in self.sessions.items():
            try:
                tools = await session.list_tools()
                print(f"\n📦 Server: {name}")
                if tools and hasattr(tools, 'tools'):
                    for tool in tools.tools:
                        print(f"   • {tool.name}: {tool.description}")
                else:
                    print("   No tools available")
            except Exception as e:
                print(f"   ❌ Error listing tools for {name}: {e}")
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Call a specific tool on a specific server"""
        if server_name not in self.sessions:
            print(f"❌ Server {server_name} not connected")
            return None
            
        session = self.sessions[server_name]
        arguments = arguments or {}
        
        try:
            result = await session.call_tool(tool_name, arguments)
            print(f"✅ Tool '{tool_name}' on server '{server_name}' executed successfully")
            return result
        except Exception as e:
            print(f"❌ Error calling tool '{tool_name}' on server '{server_name}': {e}")
            return None
    
    async def run_interactive_mode(self) -> None:
        """Run the client in interactive mode"""
        print("\n🎮 Interactive MCP Client Mode")
        print("=" * 50)
        print("Available commands:")
        print("  list-tools             - List all available tools")
        print("  call-tool <server> <tool> [args] - Call a specific tool")
        print("  servers                - List connected servers")
        print("  help                   - Show this help message")
        print("  quit                   - Exit the client")
        print("=" * 50)
        
        while True:
            try:
                command = input("\n🔧 Enter command: ").strip().split()
                
                if not command:
                    continue
                    
                if command[0] == "quit":
                    break
                elif command[0] == "help":
                    print("Available commands:")
                    print("  list-tools             - List all available tools")
                    print("  call-tool <server> <tool> [args] - Call a specific tool")
                    print("  servers                - List connected servers")
                    print("  help                   - Show this help message")
                    print("  quit                   - Exit the client")
                elif command[0] == "list-tools":
                    await self.list_all_tools()
                elif command[0] == "servers":
                    print("\n🔗 Connected Servers:")
                    print("=" * 30)
                    if self.sessions:
                        for name in self.sessions:
                            print(f"   • {name}")
                    else:
                        print("   No servers connected")
                elif command[0] == "call-tool":
                    if len(command) < 3:
                        print("Usage: call-tool <server> <tool> [args]")
                        continue
                        
                    server_name = command[1]
                    tool_name = command[2]
                    arguments: Dict[str, Any] = {}
                    
                    # Parse arguments if provided
                    if len(command) > 3:
                        try:
                            # Simple argument parsing (in a real implementation, you might want JSON)
                            for arg in command[3:]:
                                if "=" in arg:
                                    key, value = arg.split("=", 1)
                                    # Try to convert to int or float if possible
                                    try:
                                        if '.' in value:
                                            arguments[key] = float(value)
                                        else:
                                            arguments[key] = int(value)
                                    except ValueError:
                                        arguments[key] = value
                        except Exception as e:
                            print(f"Error parsing arguments: {e}")
                            continue
                    
                    await self.call_tool(server_name, tool_name, arguments)
                else:
                    print(f"Unknown command: {command[0]}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

async def main() -> None:
    """Main function to run the MCP client"""
    print("🌍 MCP Python Client")
    print("=" * 50)
    print("Connecting to servers defined in mcp.json...")
    
    try:
        # Initialize the client
        client = MCPClient("mcp.json")
        
        # Connect to all servers
        await client.connect_all_servers()
        
        # List available tools
        await client.list_all_tools()
        
        # Run interactive mode
        await client.run_interactive_mode()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())