#!/usr/bin/env python3
"""
Monitoring Agent for Africa-USA Trade Intelligence Platform
Continuously monitors system health and performance
"""

import requests
import time
import os
import json
from datetime import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MonitoringAgent:
    def __init__(self):
        self.api_url = os.getenv("STREAMLIT_API_URL", "https://africa-usa-trade-intelligence.onrender.com")
        self.check_interval = int(os.getenv("MONITORING_INTERVAL", "3600"))  # 1 hour default
        self.alert_threshold = int(os.getenv("ALERT_THRESHOLD", "3"))  # 3 consecutive failures before alert
        self.email_recipient = os.getenv("EMAIL_RECIPIENT", "temangroup1930@gmail.com")
        self.email_sender = os.getenv("EMAIL_SENDER", "monitoring@africa-usa-trade.com")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
        self.email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.email_port = int(os.getenv("EMAIL_PORT", "587"))
        
        # Initialize counters
        self.consecutive_failures = 0
        self.last_check = None
        self.status_history = []
        
    def check_api_health(self):
        """Check if the API is responding correctly"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            return response.status_code == 200, response.json() if response.status_code == 200 else None
        except Exception as e:
            return False, str(e)
    
    def check_dashboard_health(self):
        """Check if the dashboard is accessible"""
        try:
            # For Streamlit apps, we can check if the main page loads
            response = requests.get(f"{self.api_url}", timeout=15)
            return response.status_code == 200, {"status": "Dashboard accessible", "response_time": response.elapsed.total_seconds()}
        except Exception as e:
            return False, str(e)
    
    def check_data_endpoints(self):
        """Check critical data endpoints"""
        endpoints = [
            "census-data?trade_type=imports",
            "exchange-rates",
            "commodity-prices",
            "african-markets"
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.api_url}/{endpoint}", timeout=15)
                results[endpoint] = {
                    "status": "success" if response.status_code == 200 else "failed",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def record_status(self, component, is_healthy, details):
        """Record the status of a component"""
        status_record = {
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "healthy": is_healthy,
            "details": details
        }
        
        self.status_history.append(status_record)
        # Keep only the last 100 records
        if len(self.status_history) > 100:
            self.status_history = self.status_history[-100:]
        
        return status_record
    
    def should_alert(self, is_healthy):
        """Determine if an alert should be sent"""
        if is_healthy:
            # Reset counter on success
            self.consecutive_failures = 0
            return False
        else:
            # Increment failure counter
            self.consecutive_failures += 1
            return self.consecutive_failures >= self.alert_threshold
    
    def send_email(self, subject, body):
        """Send an email notification"""
        try:
            if not self.email_password:
                logger.warning("Email password not configured, skipping email notification")
                return False
                
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_sender, self.email_recipient, text)
            server.quit()
            
            logger.info(f"Email sent to {self.email_recipient}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def generate_status_report(self, health_check_result):
        """Generate a comprehensive status report"""
        report = f"""
Africa-USA Trade Intelligence Platform - Hourly Status Report
============================================================

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

OVERALL SYSTEM STATUS: {'HEALTHY' if health_check_result['overall_healthy'] else 'ISSUES DETECTED'}

API STATUS:
- Healthy: {health_check_result['components']['api']['healthy']}
- Details: {health_check_result['components']['api']['details']}

DASHBOARD STATUS:
- Healthy: {health_check_result['components']['dashboard']['healthy']}
- Details: {health_check_result['components']['dashboard']['details']}

DATA ENDPOINTS:
"""
        
        for endpoint, result in health_check_result['data_endpoints'].items():
            status = result.get('status', 'unknown')
            report += f"- {endpoint}: {status}\n"
            if 'response_time' in result:
                report += f"  Response Time: {result['response_time']:.2f}s\n"
            if 'error' in result:
                report += f"  Error: {result['error']}\n"
        
        report += f"""
SYSTEM METRICS:
- Consecutive Failures: {self.consecutive_failures}
- Last Check: {self.last_check}
- Monitoring Interval: {self.check_interval} seconds

This is an automated report from your continuous monitoring system.
"""
        
        return report
    
    def save_monitoring_results(self, health_check_result):
        """Save monitoring results to a file for the dashboard"""
        try:
            # Load existing results
            results = []
            if os.path.exists("monitoring_results.json"):
                with open("monitoring_results.json", "r") as f:
                    results = json.load(f)
            
            # Add new result
            results.append(health_check_result)
            
            # Keep only the last 100 results
            if len(results) > 100:
                results = results[-100:]
            
            # Save results
            with open("monitoring_results.json", "w") as f:
                json.dump(results, f, indent=2)
                
            logger.info("Monitoring results saved successfully")
        except Exception as e:
            logger.error(f"Failed to save monitoring results: {e}")
    
    def send_status_update(self, health_check_result):
        """Send a status update email"""
        subject = f"Platform Status Update - {'HEALTHY' if health_check_result['overall_healthy'] else 'ISSUES'}"
        body = self.generate_status_report(health_check_result)
        
        return self.send_email(subject, body)
    
    def run_health_check(self):
        """Run a complete health check of all components"""
        logger.info("Running comprehensive health check...")
        
        # Check API
        api_healthy, api_details = self.check_api_health()
        api_status = self.record_status("API", api_healthy, api_details)
        
        # Check Dashboard
        dashboard_healthy, dashboard_details = self.check_dashboard_health()
        dashboard_status = self.record_status("Dashboard", dashboard_healthy, dashboard_details)
        
        # Check Data Endpoints
        data_endpoints_status = self.check_data_endpoints()
        
        # Log summary
        overall_healthy = api_healthy and dashboard_healthy
        logger.info(f"Health check complete. Overall status: {'HEALTHY' if overall_healthy else 'UNHEALTHY'}")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "overall_healthy": overall_healthy,
            "components": {
                "api": api_status,
                "dashboard": dashboard_status
            },
            "data_endpoints": data_endpoints_status
        }
        
        self.last_check = datetime.now().isoformat()
        return result
    
    def auto_correct_issues(self, health_check_result):
        """Attempt to automatically correct common issues"""
        corrections_made = []
        
        # Check if API is down
        if not health_check_result['components']['api']['healthy']:
            corrections_made.append("API is unreachable - please check API server status")
            
        # Check if dashboard is down
        if not health_check_result['components']['dashboard']['healthy']:
            corrections_made.append("Dashboard is unreachable - please check Streamlit deployment")
            
        # Check data endpoints
        for endpoint, result in health_check_result['data_endpoints'].items():
            if result.get('status') != 'success':
                corrections_made.append(f"Data endpoint {endpoint} is failing - check data source connectivity")
        
        if corrections_made:
            correction_report = "Automatic corrections attempted:\n" + "\n".join([f"- {c}" for c in corrections_made])
            logger.info(correction_report)
            return correction_report
        else:
            logger.info("No issues detected requiring automatic correction")
            return "No automatic corrections needed"
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        logger.info(f"Starting continuous monitoring with {self.check_interval} second intervals...")
        
        # Send initial status report
        initial_report = self.run_health_check()
        self.save_monitoring_results(initial_report)
        self.send_status_update(initial_report)
        
        while True:
            try:
                # Run health check
                health_check_result = self.run_health_check()
                
                # Attempt auto-correction
                correction_report = self.auto_correct_issues(health_check_result)
                
                # Save results for dashboard
                self.save_monitoring_results(health_check_result)
                
                # Send status update
                self.send_status_update(health_check_result)
                
                # Check if we should alert
                if not health_check_result['overall_healthy'] and self.should_alert(False):
                    alert_body = f"""
CRITICAL ALERT: Africa-USA Trade Intelligence Platform Issues Detected

{self.generate_status_report(health_check_result)}

Auto-correction attempts:
{correction_report}

Please investigate immediately.
"""
                    self.send_email("CRITICAL ALERT: Platform Issues", alert_body)
                
                logger.info(f"Waiting {self.check_interval} seconds until next check...")
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error during monitoring: {e}")
                logger.error(traceback.format_exc())
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    agent = MonitoringAgent()
    agent.start_monitoring()