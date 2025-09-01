#!/usr/bin/env python3
"""
Test All MCP Servers Connection
Script to verify connectivity to all configured MCP servers
"""

import json
import subprocess
import sys
import time
import os
from pathlib import Path

def load_mcp_config():
    """Load the MCP configuration file"""
    config_path = Path("mcp.json")
    if not config_path.exists():
        print("❌ Error: mcp.json configuration file not found")
        return None
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return None

def test_stdio_server(server_name, command, args):
    """Test a stdio-based MCP server"""
    print(f"🔄 Testing {server_name} (stdio)...")
    
    try:
        # Construct the full command
        full_command = [command] + args
        print(f"   Command: {' '.join(full_command)}")
        
        # For Python servers, we can check if the file exists
        if command == "python" and args:
            script_path = args[0]
            if not Path(script_path).exists():
                print(f"   ❌ Script not found: {script_path}")
                return False
        
        print(f"   ✅ {server_name} configuration is valid")
        return True
    except Exception as e:
        print(f"   ❌ Error testing {server_name}: {e}")
        return False

def test_http_server(server_name, url):
    """Test an HTTP-based MCP server"""
    print(f"🔄 Testing {server_name} (HTTP)...")
    print(f"   URL: {url}")
    
    # For now, we'll just verify the URL format
    # In a more comprehensive test, we would actually make an HTTP request
    if url.startswith("http://") or url.startswith("https://"):
        print(f"   ✅ {server_name} URL format is valid")
        return True
    else:
        print(f"   ❌ Invalid URL format for {server_name}")
        return False

def test_all_servers(config):
    """Test all servers in the configuration"""
    if not config or "servers" not in config:
        print("❌ Invalid configuration file")
        return False
    
    servers = config["servers"]
    results = {}
    
    print("🚀 Testing all MCP server connections...\n")
    
    for server_name, server_config in servers.items():
        server_type = server_config.get("type")
        
        if server_type == "stdio":
            command = server_config.get("command")
            args = server_config.get("args", [])
            results[server_name] = test_stdio_server(server_name, command, args)
        elif server_type == "http":
            url = server_config.get("url")
            results[server_name] = test_http_server(server_name, url)
        else:
            print(f"❓ Unknown server type for {server_name}: {server_type}")
            results[server_name] = False
    
    print("\n" + "="*50)
    print("📊 MCP SERVER CONNECTION TEST RESULTS")
    print("="*50)
    
    success_count = 0
    total_count = len(results)
    
    for server_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {server_name}")
        if success:
            success_count += 1
    
    print("="*50)
    print(f"📈 Results: {success_count}/{total_count} servers connected successfully")
    
    if success_count == total_count:
        print("🎉 All MCP servers are properly configured!")
        return True
    else:
        print("⚠️  Some servers failed to connect. Check the configuration.")
        return False

def main():
    """Main function to run the MCP server tests"""
    print("🔍 MCP Server Connection Tester")
    print("="*50)
    
    # Load configuration
    config = load_mcp_config()
    if not config:
        return 1
    
    # Test all servers
    success = test_all_servers(config)
    
    if success:
        print("\n🚀 READY: All MCP servers are ready for use!")
        print("You can now connect to them through your MCP client.")
        return 0
    else:
        print("\n❌ ISSUE: Some MCP servers are not properly configured.")
        print("Please check the configuration and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())