#!/usr/bin/env python3
"""
Synthetic health check used by GitHub Actions (hourly monitor).
Writes a markdown report to .github/monitor/latest_report.md
Exit code is 0 for healthy, non-zero for unhealthy so workflows can react.
"""
import os
import sys
import time
import requests
from datetime import datetime, UTC

DEPLOYED_URL = os.environ.get(
    "DEPLOYED_URL", "https://africa-usa-trade-intelligence.onrender.com"
)
REPORT_DIR = ".github/monitor"
os.makedirs(REPORT_DIR, exist_ok=True)
report_path = os.path.join(REPORT_DIR, "latest_report.md")


def run_check():
    url = DEPLOYED_URL.rstrip("/") + "/health"
    start = time.time()
    try:
        resp = requests.get(url, timeout=15)
        elapsed = time.time() - start
        status = resp.status_code
        content = resp.text
        healthy = resp.status_code == 200
        report = f"# Health check report - {datetime.now(UTC).isoformat()}\n\n"
        report += f"- URL: {url}\n- Status code: {status}\n- Response time: {elapsed:.2f}s\n\n"
        report += "## Response body\n\n"
        report += "```\n" + content + "\n```\n"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        if not healthy:
            print("UNHEALTHY:", status)
            return 2
        print("HEALTHY")
        return 0
    except Exception as e:
        report = f"# Health check error - {datetime.now(UTC).isoformat()}\n\n- Error: {str(e)}\n"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print("EXCEPTION:", e)
        return 3


if __name__ == "__main__":
    code = run_check()
    sys.exit(code)
