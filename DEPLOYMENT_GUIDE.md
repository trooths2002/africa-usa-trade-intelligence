# Africa-USA Trade Intelligence Platform - Deployment Guide

This guide explains how to deploy the Africa-USA Trade Intelligence Platform with the production-ready config pack.

## Prerequisites

1. A GitHub repository with the latest code
2. A Render or Railway account (free tier is sufficient)
3. A PostgreSQL database (free tier option available)

## Deployment Options

### Option A: Render Deployment (Recommended)

1. Fork this repository to your GitHub account
2. Sign up for a free Render account at https://render.com
3. Connect your GitHub account to Render
4. Create a new Web Service and select your forked repository
5. Render will automatically detect the `render.yaml` file and configure two services:
   - `ausa-dashboard`: The Streamlit dashboard
   - `ausa-health`: The FastAPI health check endpoint

### Option B: Railway Deployment

1. Fork this repository to your GitHub account
2. Sign up for a free Railway account at https://railway.app
3. Connect your GitHub account to Railway
4. Create a new project and select your forked repository
5. Railway will automatically detect the `Procfile` and configure two processes:
   - `web`: The Streamlit dashboard
   - `health`: The FastAPI health check endpoint

## Environment Variables Configuration

Set these environment variables in your hosting platform:

1. `APP_LOGIN_PASSWORD` - A strong passphrase to protect your dashboard
2. `DATABASE_URL` - Your PostgreSQL database connection string
3. `STREAMLIT_API_URL` - Your deployed dashboard URL (e.g., `https://your-app.onrender.com`)

### GitHub Secrets for CI Health Checks

Set `STREAMLIT_API_URL` as a GitHub Secret for CI health checks:
1. Go to your repository Settings
2. Navigate to Secrets and variables → Actions
3. Create a new repository secret named `STREAMLIT_API_URL`
4. Set the value to your deployed dashboard URL

## Database Setup

### Local Development
The platform uses SQLite by default for local development (`sqlite:///./trade_intelligence.db`).

### Production
For production, use a PostgreSQL database:
1. On Render: Use Render's integrated PostgreSQL service
2. On Railway: Use Railway's integrated PostgreSQL service
3. Other providers: Use any PostgreSQL-compatible database service

## Monitoring and Health Checks

### Built-in Health Endpoint
The platform includes a FastAPI health check endpoint at `/health` which returns `{"status": "ok"}`.

### CI Health Checks
GitHub Actions runs a health check every 30 minutes to verify the dashboard is responsive.

### Uptime Monitoring
Set up external monitoring (e.g., UptimeRobot) to monitor:
1. Dashboard URL (e.g., `https://your-app.onrender.com`)
2. Health endpoint (e.g., `https://your-health-service.onrender.com/health`)

## Security Considerations

1. Always use a strong `APP_LOGIN_PASSWORD`
2. Restrict access to environment variables
3. Use HTTPS in production
4. Regularly update dependencies

## Troubleshooting

### Dashboard Not Loading
1. Check that `APP_LOGIN_PASSWORD` is set correctly
2. Verify the startup script permissions (should be executable)
3. Check the application logs for errors

### Health Check Failing
1. Verify the FastAPI service is running
2. Check that the port configuration is correct
3. Review the health service logs

### Database Connection Issues
1. Verify `DATABASE_URL` is set correctly
2. Ensure the database service is running
3. Check that network access is allowed

## Updating the Application

1. Push changes to your repository
2. The hosting platform will automatically redeploy
3. Monitor the deployment logs for any issues

## SMTP Email Configuration

The MCP automation workflow includes email notifications for daily summaries and alerts. Configure SMTP settings using GitHub repository secrets.

### Required GitHub Secrets

Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | SMTP username (usually your email) | `your-email@gmail.com` |
| `SMTP_PASSWORD` | SMTP password or app password | `your-app-password` |
| `NOTIFY_EMAIL_TO` | Recipient email address | `recipient@company.com` |
| `NOTIFY_EMAIL_FROM` | Sender email address | `your-email@gmail.com` |

### Gmail SMTP Configuration

For Gmail users, follow these steps:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Navigate to Security > 2-Step Verification > App passwords
   - Generate a new app password for "Mail"
   - Use this app password as `SMTP_PASSWORD` (not your regular Gmail password)

3. **Gmail SMTP Settings**:
   - `SMTP_HOST`: `smtp.gmail.com`
   - `SMTP_PORT`: `587`
   - `SMTP_USERNAME`: Your Gmail address
   - `SMTP_PASSWORD`: The generated app password

### Other Email Providers

| Provider | SMTP Host | Port | Security |
|----------|-----------|------|----------|
| Gmail | smtp.gmail.com | 587 | TLS |
| Outlook/Hotmail | smtp.live.com | 587 | TLS |
| Yahoo | smtp.mail.yahoo.com | 587 | TLS |
| iCloud | smtp.mail.me.com | 587 | TLS |

### Testing Email Configuration

1. **Manual Workflow Trigger**: Go to Actions tab in GitHub and manually trigger the "MCP Automation with SMTP Email" workflow
2. **Check Workflow Logs**: Review the workflow execution logs for any email sending errors
3. **Verify Email Receipt**: Confirm the summary email is received at the specified recipient address

### Email Content

The automated emails include:
- Daily trade data collection summary
- Market intelligence analysis results
- System health status
- Recent arbitrage opportunities
- New supplier/buyer intelligence updates

### Troubleshooting Email Issues

Common issues and solutions:

1. **Authentication Failed**: Verify app password is correct and 2FA is enabled
2. **Connection Timeout**: Check SMTP host and port settings
3. **Recipient Not Receiving**: Check spam/junk folders
4. **Invalid Credentials**: Ensure secrets are set correctly in GitHub repository

## Support

For issues with deployment, contact the development team or check the GitHub Issues section of this repository.