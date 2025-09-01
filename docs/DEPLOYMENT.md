# Africa-USA Trade Intelligence Platform - Deployment Guide

This guide covers deployment and configuration for the Africa-USA Trade Intelligence Platform, including SMTP email notifications for automated workflows.

## SMTP Configuration for GitHub Actions

### Required Secrets

Configure the following secrets in your GitHub repository settings (Settings > Secrets and variables > Actions):

- `SMTP_HOST` - SMTP server hostname
- `SMTP_PORT` - SMTP server port (typically 587 for TLS)  
- `SMTP_USERNAME` - SMTP authentication username
- `SMTP_PASSWORD` - SMTP authentication password
- `NOTIFY_EMAIL_TO` - Recipient email address for notifications
- `NOTIFY_EMAIL_FROM` - Sender email address

### Gmail SMTP Setup with App Passwords

To use Gmail SMTP for automated notifications, follow these step-by-step instructions:

#### Step 1: Enable 2-Factor Authentication
1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Navigate to "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the prompts to enable 2FA if not already enabled

#### Step 2: Generate App Password
1. In Google Account settings, go to "Security"
2. Under "Signing in to Google", click "2-Step Verification" 
3. Scroll down and click "App passwords"
4. Select "Mail" as the app and "Other (Custom name)" as the device
5. Enter "Africa-USA Trade Intelligence" as the custom name
6. Click "Generate"
7. Copy the 16-character app password (format: xxxx xxxx xxxx xxxx)

#### Step 3: Configure GitHub Secrets
Add these secrets to your GitHub repository:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-gmail-address@gmail.com
SMTP_PASSWORD=your-16-character-app-password
NOTIFY_EMAIL_TO=recipient@example.com
NOTIFY_EMAIL_FROM=your-gmail-address@gmail.com
```

**Important:** Use the 16-character app password, NOT your regular Gmail password.

### Testing SMTP Configuration

1. Navigate to Actions > MCP Automation in your GitHub repository
2. Click "Run workflow" to manually trigger the automation
3. Check that you receive the email notification
4. Review the workflow logs for any SMTP connection issues

### Alternative SMTP Providers

#### Outlook/Hotmail
```
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-outlook-email@outlook.com
SMTP_PASSWORD=your-outlook-password
```

#### Yahoo Mail
```
SMTP_HOST=smtp.mail.yahoo.com  
SMTP_PORT=587
SMTP_USERNAME=your-yahoo-email@yahoo.com
SMTP_PASSWORD=your-yahoo-app-password
```

### Troubleshooting SMTP Issues

#### Common Error: "Authentication failed"
- Verify the username and password are correct
- For Gmail, ensure you're using an app password, not your regular password
- Check that 2FA is enabled on your Google account

#### Common Error: "Connection timeout"  
- Verify the SMTP_HOST and SMTP_PORT are correct
- Check if your network/firewall blocks SMTP connections

#### Common Error: "SSL/TLS handshake failed"
- Most providers require port 587 with STARTTLS
- Ensure SMTP_PORT is set to 587, not 465 or 25

### Security Best Practices

1. **Never commit SMTP credentials to source code**
2. **Use app-specific passwords when available** (Gmail, Yahoo)
3. **Regularly rotate SMTP passwords**
4. **Monitor failed authentication attempts**
5. **Use dedicated email accounts for automation**

### Workflow Configuration

The MCP automation workflow sends email notifications:
- **On successful runs** with scan results summary
- **On failed runs** with error information  
- **Includes workflow logs** as attachments
- **Runs hourly** or can be triggered manually

Email notifications include:
- Workflow run number and status
- Quick scan results and exit codes
- Links to detailed workflow logs
- Automation log files as attachments