#!/usr/bin/env python3
"""
Test script to check the health endpoint
"""
import requests
import time
import sys

def test_health_endpoint(url):
    """
    Test the health endpoint
    """
    print(f"Testing health endpoint: {url}")
    
    try:
        start = time.time()
        response = requests.get(url, timeout=30)
        elapsed = (time.time() - start) * 1000
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed:.0f}ms")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Health endpoint is working")
            return True
        else:
            print("❌ Health endpoint returned non-200 status")
            return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    # Test both the FastAPI health endpoint and the Streamlit app
    urls = [
        "https://africa-usa-trade-intelligence.onrender.com/health",
        "https://africa-usa-trade-intelligence.onrender.com"
    ]
    
    results = []
    for url in urls:
        print(f"\n{'='*50}")
        success = test_health_endpoint(url)
        results.append((url, success))
    
    print(f"\n{'='*50}")
    print("SUMMARY:")
    for url, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {url}")

if __name__ == "__main__":
    main()