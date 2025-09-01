#!/usr/bin/env python3
"""
Test script to connect to the running MCP server at http://127.0.0.1:6010/sse
Logs all received messages to a file for analysis.
"""
import requests
import json
import time
from datetime import datetime

def test_mcp_connection():
    """Test connection to the MCP server and log received messages"""
    url = "http://127.0.0.1:6010/sse/messages"
    log_file = "mcp_server_output.log"
    
    print(f"Connecting to MCP server at: {url}")
    print(f"Logging output to: {log_file}")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    # Open log file for writing
    with open(log_file, 'w') as f:
        f.write(f"MCP Server Connection Log - {datetime.now()}\n")
        f.write(f"URL: {url}\n")
        f.write("-" * 50 + "\n")
        f.flush()
        
        try:
            # Using stream=True to handle SSE (Server-Sent Events)
            with requests.get(url, stream=True, timeout=30) as response:
                f.write(f"Status Code: {response.status_code}\n")
                f.write(f"Headers: {dict(response.headers)}\n")
                f.write("-" * 50 + "\n")
                f.flush()
                
                print(f"Status Code: {response.status_code}")
                
                # Read the stream
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Print to console
                        print(f"[{timestamp}] Received: {decoded_line}")
                        
                        # Log to file
                        f.write(f"[{timestamp}] {decoded_line}\n")
                        f.flush()
                        
        except requests.exceptions.Timeout:
            error_msg = "Connection timed out after 30 seconds"
            print(error_msg)
            with open(log_file, 'a') as f:
                f.write(f"ERROR: {error_msg}\n")
                
        except KeyboardInterrupt:
            print("\nStopping connection...")
            with open(log_file, 'a') as f:
                f.write("\nConnection stopped by user\n")
                
        except Exception as e:
            error_msg = f"Error connecting to MCP server: {e}"
            print(error_msg)
            with open(log_file, 'a') as f:
                f.write(f"ERROR: {error_msg}\n")

if __name__ == "__main__":
    test_mcp_connection()