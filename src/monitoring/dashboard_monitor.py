#!/usr/bin/env python3
"""
Dashboard Monitor for Africa-USA Trade Intelligence Platform
Provides more frequent monitoring of the dashboard functionality
"""

import requests
import time
import os
import json
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashboardMonitor:
    def __init__(self):
        self.dashboard_url = os.getenv("DASHBOARD_URL", "http://localhost:8501")
        self.api_url = os.getenv("STREAMLIT_API_URL", "https://africa-usa-trade-intelligence.onrender.com")
        self.check_interval = int(os.getenv("DASHBOARD_MONITOR_INTERVAL", "300"))  # 5 minutes default
        
    def check_dashboard_accessibility(self):
        """Check if the dashboard is accessible"""
        try:
            response = requests.get(self.dashboard_url, timeout=15)
            return response.status_code == 200, {
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "content_length": len(response.content)
            }
        except Exception as e:
            return False, {"error": str(e)}
    
    def check_dashboard_interactivity(self):
        """Check if the dashboard is interactive using Selenium"""
        try:
            # Set up Chrome options for headless browsing
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Initialize the webdriver
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            
            # Load the dashboard
            driver.get(self.dashboard_url)
            
            # Wait for key elements to load
            wait = WebDriverWait(driver, 10)
            
            # Check for main header
            header = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Africa-USA Trade Intelligence')]")))
            
            # Check for API status expander
            api_status_expander = driver.find_element(By.XPATH, "//div[contains(text(), 'API Service Status')]")
            
            # Check for report form
            report_form = driver.find_element(By.XPATH, "//form[@data-testid='stForm']")
            
            driver.quit()
            
            return True, {
                "header_found": header is not None,
                "api_status_found": api_status_expander is not None,
                "report_form_found": report_form is not None,
                "selenium_check": "passed"
            }
        except Exception as e:
            logger.error(f"Selenium check failed: {e}")
            logger.error(traceback.format_exc())
            return False, {"error": str(e), "selenium_check": "failed"}
    
    def check_api_connectivity(self):
        """Check if the dashboard can connect to the API"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            return response.status_code == 200, {
                "api_status": response.status_code,
                "api_response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return False, {"error": str(e)}
    
    def run_comprehensive_check(self):
        """Run a comprehensive dashboard check"""
        logger.info("Running comprehensive dashboard check...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Check dashboard accessibility
        accessible, access_details = self.check_dashboard_accessibility()
        results["checks"]["accessibility"] = {
            "passed": accessible,
            "details": access_details
        }
        
        # Check API connectivity
        api_connected, api_details = self.check_api_connectivity()
        results["checks"]["api_connectivity"] = {
            "passed": api_connected,
            "details": api_details
        }
        
        # Check dashboard interactivity (only if accessible)
        if accessible:
            interactive, interactive_details = self.check_dashboard_interactivity()
            results["checks"]["interactivity"] = {
                "passed": interactive,
                "details": interactive_details
            }
        else:
            results["checks"]["interactivity"] = {
                "passed": False,
                "details": {"reason": "Dashboard not accessible, skipping interactivity check"}
            }
        
        # Overall health
        overall_healthy = all(check["passed"] for check in results["checks"].values())
        results["overall_healthy"] = overall_healthy
        
        logger.info(f"Dashboard check complete. Status: {'HEALTHY' if overall_healthy else 'ISSUES'}")
        return results
    
    def start_monitoring(self):
        """Start continuous dashboard monitoring"""
        logger.info(f"Starting dashboard monitoring with {self.check_interval} second intervals...")
        
        while True:
            try:
                results = self.run_comprehensive_check()
                
                # Log results
                status = "HEALTHY" if results["overall_healthy"] else "ISSUES DETECTED"
                logger.info(f"Dashboard Status: {status}")
                
                # Save results to file for debugging
                with open("dashboard_monitor_results.json", "w") as f:
                    json.dump(results, f, indent=2)
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Dashboard monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error during dashboard monitoring: {e}")
                logger.error(traceback.format_exc())
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    monitor = DashboardMonitor()
    monitor.start_monitoring()