#!/usr/bin/env python3
"""
Script to set up UptimeRobot monitoring for the Africa-USA Trade Intelligence Platform
"""

import requests
import os
import sys
from src.config.settings import STREAMLIT_API_URL

def setup_uptime_robot_monitoring():
    """
    Set up UptimeRobot monitors for the platform
    """
    # Get UptimeRobot API key from environment
    api_key = os.getenv("UPTIMEROBOT_API_KEY")
    if not api_key:
        print("UPTIMEROBOT_API_KEY not found in environment variables")
        print("Please set UptimeRobot API key as a GitHub secret and try again")
        return False
    
    # Define monitors to create
    monitors = [
        {
            "friendly_name": "Africa-USA Trade Intelligence Dashboard",
            "url": STREAMLIT_API_URL,
            "type": 1,  # HTTP(s)
            "interval": 300  # 5 minutes
        },
        {
            "friendly_name": "Africa-USA Trade Intelligence API Health",
            "url": f"{STREAMLIT_API_URL}/health",
            "type": 1,  # HTTP(s)
            "interval": 300  # 5 minutes
        }
    ]
    
    # UptimeRobot API endpoint
    api_url = "https://api.uptimerobot.com/v2/newMonitor"
    
    headers = {
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded"
    }
    
    success_count = 0
    
    for monitor in monitors:
        # Prepare payload
        payload = {
            "api_key": api_key,
            "friendly_name": monitor["friendly_name"],
            "url": monitor["url"],
            "type": monitor["type"],
            "interval": monitor["interval"]
        }
        
        try:
            response = requests.post(api_url, data=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if result.get("stat") == "ok":
                    print(f"✓ Successfully created monitor: {monitor['friendly_name']}")
                    success_count += 1
                else:
                    print(f"✗ Failed to create monitor: {monitor['friendly_name']}")
                    print(f"  Error: {result.get('error', {}).get('message', 'Unknown error')}")
            else:
                print(f"✗ HTTP error {response.status_code} when creating monitor: {monitor['friendly_name']}")
        except Exception as e:
            print(f"✗ Exception when creating monitor {monitor['friendly_name']}: {e}")
    
    print(f"\nSuccessfully set up {success_count}/{len(monitors)} monitors")
    return success_count == len(monitors)

if __name__ == "__main__":
    if setup_uptime_robot_monitoring():
        print("\n✅ UptimeRobot monitoring setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ UptimeRobot monitoring setup failed!")
        sys.exit(1)