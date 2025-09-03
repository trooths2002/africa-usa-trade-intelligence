import os
import requests
import sys
import time


def main():
    url = os.getenv("STREAMLIT_API_URL")
    if not url:
        print("STREAMLIT_API_URL not set")
        sys.exit(2)
    start = time.time()
    try:
        # Ensure trailing slash removed and add /health
        health_url = url.rstrip("/") + "/health"
        resp = requests.get(health_url, timeout=10)
        dt = int((time.time() - start) * 1000)
        if resp.status_code == 200:
            print(f"Dashboard healthy: {resp.status_code} ({dt}ms)")
            sys.exit(0)
        else:
            print(f"Dashboard unhealthy: {resp.status_code} ({dt}ms) - {resp.text[:200]}")
            sys.exit(1)
    except Exception as e:
        dt = int((time.time() - start) * 1000)
        print(f"Error: {e} ({dt}ms)")
        sys.exit(1)


if __name__ == "__main__":
    main()
