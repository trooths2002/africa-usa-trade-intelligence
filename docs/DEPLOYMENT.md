# Africa-USA Trade Intelligence Platform - Deployment Guide

This guide explains how to deploy and run the Africa-USA Trade Intelligence Platform with real-time data capabilities.

## Architecture Overview

The platform consists of three main components:

1. **MCP API Server** - A FastAPI web service that provides real-time data with caching
2. **Streamlit Dashboard** - The user interface for viewing market intelligence
3. **Monitoring Service** - Ensures all services are running properly

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd free-world-trade
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Services

### Option 1: Using the Startup Script (Recommended)

Run all services with the startup script:
```bash
python start_services.py
```

This will start:
- MCP API Server on http://localhost:8000
- Streamlit Dashboard on http://localhost:8501

### Option 2: Manual Startup

1. Start the MCP API Server:
   ```bash
   python src/mcp_servers/market_intelligence/api_server.py
   ```

2. In a separate terminal, start the Streamlit Dashboard:
   ```bash
   streamlit run src/web_app/dashboard/deployed_main.py
   ```

### Option 3: Using Process Managers

For production deployments, consider using process managers like `supervisor` or `pm2`.

## Service URLs

- **API Server**: http://localhost:8000
- **Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## Monitoring

Start the monitoring service to ensure all components are working:
```bash
python monitor_services.py
```

## Caching Mechanism

The platform implements a simple in-memory caching system:

- **Census Data**: Cached for 30 minutes
- **Exchange Rates**: Cached for 60 minutes
- **Commodity Prices**: Cached for 30 minutes
- **Trade News**: Cached for 60 minutes
- **Weather Data**: Cached for 15 minutes

## Troubleshooting

### API Server Not Starting

1. Check if port 8000 is already in use:
   ```bash
   netstat -an | grep 8000
   ```

2. Kill any processes using port 8000:
   ```bash
   # On Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # On Linux/Mac
   lsof -i :8000
   kill -9 <PID>
   ```

### Dashboard Not Loading

1. Check if port 8501 is already in use:
   ```bash
   netstat -an | grep 8501
   ```

2. Kill any processes using port 8501 or start dashboard on a different port:
   ```bash
   streamlit run src/web_app/dashboard/deployed_main.py --server.port=8502
   ```

### Data Not Loading

1. Check API server logs for errors
2. Verify internet connectivity
3. Check if external APIs are accessible:
   - US Census Bureau API
   - World Bank API
   - Exchange rate services

## Updating the Platform

1. Pull the latest changes:
   ```bash
   git pull origin main
   ```

2. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Restart services

## Customization

### Changing API Endpoints

Modify the API base URL in `src/web_app/dashboard/deployed_main.py`:
```python
API_BASE_URL = "http://your-api-server.com:8000"
```

### Adjusting Cache Durations

Modify cache durations in `src/mcp_servers/market_intelligence/api_server.py`:
```python
@app.get("/exchange-rates")
@cached(expiry_minutes=60)  # Change this value
```

## Security Considerations

For production deployments:

1. Restrict CORS origins in `api_server.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Specific domains only
       # ...
   )
   ```

2. Add authentication for API endpoints if needed

3. Use HTTPS in production

## Scaling Considerations

For high-traffic deployments:

1. Use a proper caching solution like Redis instead of in-memory cache
2. Deploy API server and dashboard on separate machines
3. Use a load balancer for multiple instances
4. Implement database persistence for caching

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

For issues or questions, contact the development team or check the documentation.