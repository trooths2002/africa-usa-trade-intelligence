"""
Health monitoring for the Africa-USA Trade Intelligence Platform
"""
import requests
from typing import Dict, Any
import time
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HealthMonitor:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
    
    def check_api_health(self) -> Dict[str, Any]:
        """Check if the API service is healthy"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def check_dashboard_health(self) -> Dict[str, Any]:
        """Check if the dashboard is accessible"""
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def check_all_services(self) -> Dict[str, Any]:
        """Check health of all services"""
        return {
            "api": self.check_api_health(),
            "dashboard": self.check_dashboard_health(),
            "overall_status": "healthy" if (
                self.check_api_health()["status"] == "healthy" and 
                self.check_dashboard_health()["status"] == "healthy"
            ) else "unhealthy"
        }

if __name__ == "__main__":
    monitor = HealthMonitor()
    print(monitor.check_all_services())