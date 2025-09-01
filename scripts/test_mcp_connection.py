#!/usr/bin/env python3
"""
Test script to connect to the running MCP server at http://127.0.0.1:6010/sse
"""
import requests
import json
import time

def test_mcp_connection():
    """Test connection to the MCP server and display received messages"""
    url = "http://127.0.0.1:6010/sse/messages"
    
    print("Connecting to MCP server at:", url)
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Using stream=True to handle SSE (Server-Sent Events)
        with requests.get(url, stream=True) as response:
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {response.headers}")
            print("-" * 50)
            
            # Read the stream
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"Received: {decoded_line}")
                    
    except KeyboardInterrupt:
        print("\nStopping connection...")
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")

if __name__ == "__main__":
    test_mcp_connection()