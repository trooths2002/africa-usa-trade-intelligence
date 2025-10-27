# Africa-USA Trade Intelligence Platform - Automation Guide

This guide covers the automated workflows and SMTP-based notifications for the Africa-USA Trade Intelligence Platform.

## Overview

The platform includes automated workflows that run market intelligence scans and send email notifications with results. These workflows are powered by GitHub Actions and use SMTP email delivery instead of third-party services for maximum reliability and cost-effectiveness.

## Automation Workflows

### MCP Automation Workflow

**File:** `.github/workflows/mcp-automation.yml`

**Schedule:** Runs every hour and can be manually triggered

**Functions:**
- Performs quick market intelligence scans
- Generates summary reports
- Uploads execution logs as artifacts  
- Sends email notifications via SMTP

**Key Features:**
- Non-blocking execution (continues even if scan fails)
- Comprehensive logging and artifact collection
- SMTP-based email notifications
- Configurable via GitHub secrets

## SMTP-Based Notifications

The platform uses SMTP email delivery for reliable notifications without dependency on third-party email services like SendGrid. This approach provides:

✅ **No external service costs**  
✅ **Reliable delivery via standard email providers**  
✅ **Easy configuration with existing email accounts**  
✅ **Support for all major email providers (Gmail, Outlook, Yahoo, etc.)**

### Email Notification Content

Automated emails include:
- **Workflow status** and run information
- **Market scan results** summary  
- **Error information** if applicable
- **Workflow logs** as attachments
- **Direct links** to GitHub Actions runs

## Required Secrets Configuration

Configure these secrets in GitHub repository settings (Settings > Secrets and variables > Actions):

### Core SMTP Settings
| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | SMTP authentication username | `your-email@gmail.com` |
| `SMTP_PASSWORD` | SMTP authentication password | `your-app-password` |

### Email Configuration  
| Secret Name | Description | Example |
|-------------|-------------|---------|
| `NOTIFY_EMAIL_TO` | Recipient email address | `alerts@yourdomain.com` |
| `NOTIFY_EMAIL_FROM` | Sender email address | `automation@yourdomain.com` |

## Setup Instructions

### 1. Configure Email Provider

#### For Gmail Users:
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password for "Mail" application
3. Use the 16-character app password (not your regular password)

#### For Other Providers:
- **Outlook:** Use regular account credentials or app password
- **Yahoo:** Requires app password with 2FA enabled
- **Corporate Email:** Contact IT for SMTP settings

### 2. Add GitHub Secrets

1. Go to repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add each required secret from the table above
4. Verify all 6 secrets are configured

### 3. Test the Workflow

1. Navigate to Actions > MCP Automation
2. Click "Run workflow" 
3. Monitor the workflow execution
4. Verify you receive the email notification
5. Check workflow logs for any issues

## Automation Scripts

### scripts/automation/run_quick_scan.py
**Purpose:** Main automation script that performs market intelligence scans

**Features:**
- Market data collection and analysis
- Arbitrage opportunity detection
- Error handling and logging
- JSON report generation

**Output Files:**
- `automation_logs.log` - Execution logs
- `scan_report.json` - Structured scan results

### scripts/automation/send_email_summary.py  
**Purpose:** Email content generation and formatting

**Features:**
- Processes scan reports
- Generates email subject lines
- Formats HTML email content
- Creates email summary files

**Output Files:**
- `email_summary.json` - Formatted email content

## Testing and Troubleshooting

### Manual Testing
```bash
# Test the scan script locally
python scripts/automation/run_quick_scan.py

# Test email summary generation
python scripts/automation/send_email_summary.py
```

### Common Issues

#### "Authentication failed" Error
- Verify SMTP credentials are correct
- For Gmail, ensure using app password not regular password
- Check 2FA is enabled for providers that require it

#### "No email received" Issue  
- Check spam/junk folders
- Verify NOTIFY_EMAIL_TO address is correct
- Review workflow logs for SMTP errors

#### "Workflow fails immediately"
- Check all required secrets are configured
- Verify Python script syntax
- Review GitHub Actions logs for detailed errors

## Monitoring and Maintenance

### Workflow Monitoring
- Workflows run hourly automatically
- Manual triggers available via GitHub Actions UI
- Email notifications sent regardless of success/failure status
- Logs retained for 30 days via GitHub artifacts

### Log Analysis
- Workflow logs available in GitHub Actions interface
- Automation logs included as email attachments  
- JSON reports provide structured data for analysis

### Performance Optimization
- Scripts designed for quick execution (< 5 minutes)
- Non-blocking execution prevents workflow timeouts
- Efficient logging minimizes artifact storage usage

## Future Enhancements

Planned improvements to the automation system:

- **Enhanced market analysis algorithms**
- **Integration with additional data sources**  
- **Advanced notification filtering**
- **Dashboard integration for real-time monitoring**
- **Mobile notifications via Telegram/Discord**

## Support

For automation issues:

1. **Check workflow logs** in GitHub Actions
2. **Review email delivery** in spam folders  
3. **Verify secret configuration** in repository settings
4. **Test scripts locally** for debugging
5. **Consult docs/DEPLOYMENT.md** for SMTP setup details