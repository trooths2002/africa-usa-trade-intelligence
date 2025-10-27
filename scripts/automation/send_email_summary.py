#!/usr/bin/env python3
"""
Email Summary Generator for Africa-USA Trade Intelligence Platform

This script processes scan reports and generates email summaries
for automated notifications.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

def load_scan_report():
    """Load the latest scan report"""
    report_file = Path("scan_report.json")
    
    if not report_file.exists():
        logger.warning("No scan report found")
        return None
    
    try:
        with open(report_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load scan report: {e}")
        return None

def generate_email_subject(report_data):
    """Generate email subject line"""
    if not report_data:
        return "Africa-USA Trade Intelligence - Scan Failed"
    
    status = report_data.get("status", "unknown")
    if status == "success":
        return "Africa-USA Trade Intelligence - Quick Scan Complete ✅"
    else:
        return "Africa-USA Trade Intelligence - Scan Alert ⚠️"

def generate_email_body(report_data):
    """Generate email body content"""
    if not report_data:
        return """
        <h2>Quick Scan Report - Error</h2>
        <p>Unable to generate scan report. Please check the automation logs.</p>
        """
    
    scan_time = report_data.get("scan_time", "Unknown")
    status = report_data.get("status", "unknown")
    summary = report_data.get("summary", "No summary available")
    
    return f"""
    <h2>Africa-USA Trade Intelligence - Quick Scan Report</h2>
    <p><strong>Scan Time:</strong> {scan_time}</p>
    <p><strong>Status:</strong> {status.title()}</p>
    <p><strong>Summary:</strong> {summary}</p>
    
    <hr>
    <p><em>This is an automated report from the Africa-USA Trade Intelligence Platform</em></p>
    """

def generate_email_summary():
    """Generate email summary for automation workflow"""
    logger.info("Generating email summary...")
    
    # Load scan data
    report_data = load_scan_report()
    
    # Generate email content
    subject = generate_email_subject(report_data)
    body = generate_email_body(report_data)
    
    # Save email content for workflow to use
    email_content = {
        "subject": subject,
        "body": body
    }
    
    email_file = Path("email_summary.json")
    with open(email_file, 'w') as f:
        json.dump(email_content, f, indent=2)
    
    logger.info(f"Email summary saved to {email_file}")
    return email_content

def main():
    """Main function for standalone execution"""
    logging.basicConfig(level=logging.INFO)
    
    try:
        email_content = generate_email_summary()
        print("Email summary generated successfully")
        print(f"Subject: {email_content['subject']}")
        return True
    except Exception as e:
        logger.error(f"Failed to generate email summary: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)