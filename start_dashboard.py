#!/usr/bin/env python3
"""
Script to start the Africa-USA Trade Intelligence Dashboard
"""

import subprocess
import sys
import os

def main():
    """Start the Streamlit dashboard"""
    # Get the path to the main dashboard file
    dashboard_path = os.path.join("src", "web_app", "dashboard", "main.py")
    
    # Check if the file exists
    if not os.path.exists(dashboard_path):
        print(f"Error: Dashboard file not found at {dashboard_path}")
        sys.exit(1)
    
    # Start the Streamlit app
    try:
        subprocess.run([
            "streamlit", 
            "run", 
            dashboard_path,
            "--server.port", "8501"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit app: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install it with 'pip install streamlit'")
        sys.exit(1)

if __name__ == "__main__":
    main()