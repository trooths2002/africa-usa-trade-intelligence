#!/usr/bin/env python3
"""
Email Summary Sender for MCP Automation Pipeline
Sends email summaries using SMTP (no SendGrid required for free operation)
"""

import argparse
import json
import os
import sys
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email_summary.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

class EmailSender:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('NOTIFY_EMAIL_FROM', self.smtp_username)
        self.to_email = os.getenv('NOTIFY_EMAIL_TO', '')
        
        # SendGrid fallback (if configured)
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY', '')
        
        # Validate configuration
        self.is_configured = bool(self.to_email and self.from_email)
        
        if not self.is_configured:
            logger.warning("Email configuration incomplete. Set NOTIFY_EMAIL_TO and NOTIFY_EMAIL_FROM.")
    
    def load_scan_results(self) -> Optional[Dict[str, Any]]:
        """Load the latest scan results"""
        try:
            with open('logs/latest_scan_results.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("No scan results file found")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error reading scan results: {e}")
            return None
    
    def load_opportunities(self) -> Optional[list]:
        """Load the latest opportunities"""
        try:
            with open('logs/latest_opportunities.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error reading opportunities: {e}")
            return []
    
    def create_html_summary(self, scan_results: Dict[str, Any], opportunities: list, 
                           status: str, run_id: str, workflow_url: str) -> str:
        """Create HTML email summary"""
        
        # Status styling
        status_colors = {
            'success': '#28a745',
            'healthy': '#28a745',
            'partial': '#ffc107',
            'degraded': '#fd7e14',
            'failure': '#dc3545',
            'failed': '#dc3545'
        }
        
        status_color = status_colors.get(status, '#6c757d')
        
        # Count successful checks
        successful_checks = len([c for c in scan_results.get('checks', []) if c['status'] == 'success'])
        total_checks = len(scan_results.get('checks', []))
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ background-color: white; border-radius: 10px; padding: 30px; max-width: 600px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 25px; }}
                .status {{ padding: 10px 15px; border-radius: 25px; color: white; background-color: {status_color}; display: inline-block; font-weight: bold; }}
                .metric {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2a5298; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2a5298; }}
                .metric-label {{ font-size: 14px; color: #6c757d; margin-top: 5px; }}
                .opportunities {{ margin: 20px 0; }}
                .opportunity {{ background-color: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }}
                .checks-summary {{ margin: 20px 0; }}
                .check-item {{ padding: 8px 12px; margin: 5px 0; border-radius: 5px; }}
                .check-success {{ background-color: #d4edda; color: #155724; }}
                .check-warning {{ background-color: #fff3cd; color: #856404; }}
                .check-failed {{ background-color: #f8d7da; color: #721c24; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 14px; }}
                .button {{ background-color: #2a5298; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌍 Africa-USA Trade Intelligence</h1>
                    <h2>Automation Pipeline Report</h2>
                    <div class="status">{status.title()} Status</div>
                </div>
                
                <div class="metric">
                    <div class="metric-value">{successful_checks}/{total_checks}</div>
                    <div class="metric-label">Checks Passed</div>
                </div>
                
                <div class="metric">
                    <div class="metric-value">{scan_results.get('opportunities_found', 0)}</div>
                    <div class="metric-label">Opportunities Found</div>
                </div>
                
                <div class="metric">
                    <div class="metric-value">{scan_results.get('data_sources_checked', 0)}</div>
                    <div class="metric-label">Data Sources Checked</div>
                </div>
        """
        
        # Add opportunities section
        if opportunities:
            html += """
                <div class="opportunities">
                    <h3>🔥 Latest Opportunities</h3>
            """
            for opp in opportunities[:3]:  # Show top 3
                html += f"""
                    <div class="opportunity">
                        <strong>{opp.get('product', 'Unknown Product')}</strong> from {opp.get('origin', 'Unknown')}
                        <br>Price Arbitrage: {opp.get('arbitrage', 0):.1f}%
                    </div>
                """
            html += "</div>"
        
        # Add checks summary
        html += """
            <div class="checks-summary">
                <h3>📋 System Checks</h3>
        """
        
        for check in scan_results.get('checks', [])[:10]:  # Show latest 10 checks
            check_class = f"check-{check['status']}"
            status_icon = "✅" if check['status'] == 'success' else "⚠️" if check['status'] == 'warning' else "❌"
            html += f"""
                <div class="check-item {check_class}">
                    {status_icon} {check['name']}: {check['status'].title()}
                    {f" - {check['details']}" if check.get('details') else ""}
                </div>
            """
        
        # Add errors section
        if scan_results.get('errors'):
            html += """
                <div class="checks-summary">
                    <h3>❌ Errors</h3>
            """
            for error in scan_results['errors']:
                html += f'<div class="check-item check-failed">❌ {error}</div>'
            html += "</div>"
        
        # Footer with links
        html += f"""
                <div class="footer">
                    <a href="{workflow_url}" class="button">View Full Workflow</a>
                    <br><br>
                    <p>Run ID: {run_id} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                    <p>🚀 Automated by Africa-USA Trade Intelligence Platform</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def create_text_summary(self, scan_results: Dict[str, Any], opportunities: list, 
                           status: str, run_id: str, workflow_url: str) -> str:
        """Create plain text email summary"""
        
        successful_checks = len([c for c in scan_results.get('checks', []) if c['status'] == 'success'])
        total_checks = len(scan_results.get('checks', []))
        
        text = f"""
🌍 AFRICA-USA TRADE INTELLIGENCE - AUTOMATION REPORT

Status: {status.upper()}
Run ID: {run_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

📊 SUMMARY
----------
✅ Checks Passed: {successful_checks}/{total_checks}
🔥 Opportunities Found: {scan_results.get('opportunities_found', 0)}
🌐 Data Sources Checked: {scan_results.get('data_sources_checked', 0)}

"""
        
        # Add opportunities
        if opportunities:
            text += "🔥 LATEST OPPORTUNITIES\n"
            text += "---------------------\n"
            for opp in opportunities[:3]:
                text += f"• {opp.get('product', 'Unknown')} from {opp.get('origin', 'Unknown')} - {opp.get('arbitrage', 0):.1f}% arbitrage\n"
            text += "\n"
        
        # Add system checks
        text += "📋 SYSTEM CHECKS\n"
        text += "---------------\n"
        for check in scan_results.get('checks', [])[:10]:
            status_symbol = "✅" if check['status'] == 'success' else "⚠️" if check['status'] == 'warning' else "❌"
            text += f"{status_symbol} {check['name']}: {check['status'].title()}"
            if check.get('details'):
                text += f" - {check['details']}"
            text += "\n"
        
        # Add errors
        if scan_results.get('errors'):
            text += "\n❌ ERRORS\n"
            text += "--------\n"
            for error in scan_results['errors']:
                text += f"❌ {error}\n"
        
        text += f"\n🔗 View Full Report: {workflow_url}\n"
        text += "\n🚀 Automated by Africa-USA Trade Intelligence Platform"
        
        return text
    
    def send_email_smtp(self, subject: str, text_body: str, html_body: str, attachments: list = None) -> bool:
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {self.to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email via SMTP: {e}")
            return False
    
    def send_summary(self, status: str, run_id: str, workflow_url: str) -> bool:
        """Send email summary"""
        if not self.is_configured:
            logger.warning("Email not configured, skipping email notification")
            print("EMAIL_CONFIGURED=false")
            return False
        
        # Load data
        scan_results = self.load_scan_results()
        if not scan_results:
            logger.error("No scan results available")
            return False
        
        opportunities = self.load_opportunities() or []
        
        # Create email content
        subject = f"🌍 Trade Intelligence Report - {status.title()} | Run #{run_id}"
        text_body = self.create_text_summary(scan_results, opportunities, status, run_id, workflow_url)
        html_body = self.create_html_summary(scan_results, opportunities, status, run_id, workflow_url)
        
        # Prepare log attachments
        attachments = []
        for log_file in ['logs/quick_scan.log', 'logs/latest_scan_results.json', 'logs/latest_opportunities.json']:
            if os.path.exists(log_file):
                attachments.append(log_file)
        
        # Send email
        success = self.send_email_smtp(subject, text_body, html_body, attachments)
        
        print(f"EMAIL_SENT={success}")
        return success

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Send email summary of MCP automation run')
    parser.add_argument('--status', required=True, help='Status of the automation run')
    parser.add_argument('--run-id', required=True, help='GitHub Actions run ID')
    parser.add_argument('--workflow-url', required=True, help='URL to the workflow run')
    
    args = parser.parse_args()
    
    sender = EmailSender()
    success = sender.send_summary(args.status, args.run_id, args.workflow_url)
    
    if success:
        logger.info("Email summary sent successfully")
        sys.exit(0)
    else:
        logger.warning("Email summary could not be sent")
        sys.exit(0)  # Don't fail the workflow if email fails

if __name__ == "__main__":
    main()