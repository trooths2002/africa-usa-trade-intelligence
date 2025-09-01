# Deployment Guide - Africa-USA Trade Intelligence Platform

This guide provides step-by-step instructions for deploying the Africa-USA Trade Intelligence Platform with automated CI/CD pipeline and hosting setup.

## 🔐 Required GitHub Secrets

Before deploying, you need to add the following secrets to your GitHub repository. Go to your repository → Settings → Secrets and variables → Actions.

### Core Secrets (Required for basic automation)

| Secret Name | Description | Example/Notes |
|-------------|-------------|---------------|
| `NOTIFY_EMAIL_TO` | Email address to receive automation reports | `your.email@domain.com` |
| `NOTIFY_EMAIL_FROM` | Email address to send from | `noreply@yourdomain.com` |
| `SMTP_SERVER` | SMTP server for email notifications | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (usually 587 for TLS) | `587` |
| `SMTP_USERNAME` | SMTP username (often same as email) | `your.email@gmail.com` |
| `SMTP_PASSWORD` | SMTP password or app-specific password | `your-app-password` |

### Docker Hub Secrets (Required for containerized deployment)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username | Register at hub.docker.com |
| `DOCKERHUB_TOKEN` | Docker Hub access token | Docker Hub → Account Settings → Security |

### Render Deployment Secrets (For cloud hosting)

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `RENDER_API_KEY` | Render API key for deployments | Render Dashboard → API Keys |
| `RENDER_SERVICE_ID` | Market Intelligence service ID | Create service on Render, copy ID from URL |
| `RENDER_DASHBOARD_SERVICE_ID` | Dashboard service ID | Create second service on Render |

### LinkedIn Integration Secrets (For social media automation)

| Secret Name | Description | Status |
|-------------|-------------|--------|
| `LINKEDIN_CLIENT_ID` | LinkedIn app client ID | ⚠️ Manual approval required |
| `LINKEDIN_CLIENT_SECRET` | LinkedIn app client secret | ⚠️ Manual approval required |

### Additional Integration Secrets (Optional)

| Secret Name | Description | Notes |
|-------------|-------------|--------|
| `BUFFER_API_KEY` | Buffer social media API key | For automated posting |
| `MEMORY_FILE_PATH` | Path to memory storage file | `/app/data/memory.json` |

## 📧 Setting Up Email Notifications

### Option 1: Gmail SMTP (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Create an App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Add these secrets**:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your.email@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   NOTIFY_EMAIL_FROM=your.email@gmail.com
   NOTIFY_EMAIL_TO=your.email@gmail.com
   ```

### Option 2: Other SMTP Providers

| Provider | SMTP Server | Port | Notes |
|----------|-------------|------|--------|
| Outlook | smtp.live.com | 587 | Use app password |
| Yahoo | smtp.mail.yahoo.com | 587 | Use app password |
| Custom | your.smtp.server | 587/465 | Check provider docs |

## 🏗️ Hosting Options

### Option 1: Render (Recommended for Production)

**Pros**: Free tier available, automatic HTTPS, easy deployment
**Cons**: Cold starts on free tier

#### Setup Steps:

1. **Create Render Account**: Go to render.com and sign up
2. **Create Market Intelligence Service**:
   - New → Web Service
   - Connect GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python src/intelligence/server.py`
   - Add environment variables as needed
   - Copy Service ID from URL for `RENDER_SERVICE_ID`

3. **Create Dashboard Service**:
   - New → Web Service
   - Same repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run src/web_app/dashboard/main.py --server.port $PORT --server.headless true`
   - Copy Service ID for `RENDER_DASHBOARD_SERVICE_ID`

4. **Get Render API Key**:
   - Render Dashboard → Account Settings → API Keys
   - Create new API key
   - Add as `RENDER_API_KEY` secret

### Option 2: Fly.io

**Pros**: More generous free tier, better performance
**Cons**: Slightly more complex setup

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `flyctl auth login`
3. Deploy: `flyctl deploy`

### Option 3: Railway

**Pros**: Simple deployment, good free tier
**Cons**: Limited to $5 free credit per month

1. Connect GitHub repository to Railway
2. Auto-deploy on push to main
3. Set environment variables in Railway dashboard

### Option 4: Streamlit Community Cloud (Dashboard Only)

**Pros**: Free hosting for Streamlit apps
**Cons**: Only hosts the dashboard, not the full system

1. Go to share.streamlit.io
2. Connect GitHub repository
3. Set main file path: `src/web_app/dashboard/main.py`
4. Deploy

## 🐳 Local Development with Docker

### Prerequisites

- Docker and Docker Compose installed
- Clone the repository
- Create `.env` file from `.env.example`

### Quick Start

```bash
# Clone repository
git clone https://github.com/trooths2002/africa-usa-trade-intelligence.git
cd africa-usa-trade-intelligence

# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access services
# Dashboard: http://localhost:8501
# Market Intelligence API: http://localhost:8000
# Memory Server: http://localhost:3001
```

### Individual Service Commands

```bash
# Start only dashboard
docker-compose up dashboard

# Start only market intelligence
docker-compose up market_intelligence

# Rebuild after code changes
docker-compose build

# Stop all services
docker-compose down

# Clean restart
docker-compose down && docker-compose build && docker-compose up -d
```

## 🤖 Setting Up GitHub Secrets (Step-by-Step)

### For Non-Technical Users:

1. **Go to your GitHub repository**
   - Navigate to github.com/trooths2002/africa-usa-trade-intelligence

2. **Click on "Settings" tab** (next to Code, Issues, etc.)

3. **Click "Secrets and variables" in left sidebar**

4. **Click "Actions"**

5. **For each secret, click "New repository secret"**:
   - Enter "Name" (exactly as shown in tables above)
   - Enter "Secret" value
   - Click "Add secret"

6. **Start with these essential secrets**:
   ```
   NOTIFY_EMAIL_TO = your.email@gmail.com
   NOTIFY_EMAIL_FROM = your.email@gmail.com
   SMTP_SERVER = smtp.gmail.com
   SMTP_PORT = 587
   SMTP_USERNAME = your.email@gmail.com
   SMTP_PASSWORD = your-gmail-app-password
   ```

### Testing Your Setup

After adding secrets, the automation will start running hourly. You can also trigger it manually:

1. Go to "Actions" tab in your repository
2. Click "MCP Automation Pipeline"
3. Click "Run workflow"
4. Check your email for the automation report

## 🔧 Configuration Files

### Environment Variables (.env)

```bash
# Server Configuration
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
STREAMLIT_SERVER_PORT=8501

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/africa_trade

# External APIs
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
BUFFER_API_KEY=your_buffer_api_key

# Memory and Data
MEMORY_FILE_PATH=/app/data/memory.json

# Email Settings (for local development)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password
```

## 📊 Monitoring and Maintenance

### Automated Monitoring

The system includes several automated monitoring features:

1. **Hourly Health Checks**: Automated pipeline runs every hour
2. **Email Reports**: Summary emails sent after each automation run
3. **GitHub Actions Logs**: Detailed logs stored as artifacts
4. **Error Alerting**: Failed runs trigger email notifications

### Manual Monitoring

Check these regularly:

- GitHub Actions results
- Email automation reports
- Docker container health (if using Docker)
- Hosting platform dashboards

### Troubleshooting Common Issues

#### Email Not Working
```bash
# Test SMTP settings locally
python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your.email@gmail.com', 'your-app-password')
print('SMTP connection successful!')
server.quit()
"
```

#### Docker Issues
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs dashboard
docker-compose logs market_intelligence

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down --volumes && docker-compose build --no-cache && docker-compose up -d
```

#### GitHub Actions Failing
1. Check the Actions tab for error details
2. Verify all required secrets are set correctly
3. Check if dependencies are up to date
4. Review recent code changes for issues

## 🚀 Next Steps After Setup

### Immediate Actions (First 24 Hours)

1. **Verify automation is working**:
   - Check you receive hourly email reports
   - Monitor GitHub Actions for successful runs
   - Test the dashboard locally with `docker-compose up`

2. **Configure hosting**:
   - Deploy to Render or your chosen platform
   - Test deployed services are accessible
   - Configure domain name (if desired)

3. **Review data sources**:
   - Verify external APIs are accessible
   - Check data collection is working
   - Review opportunities being detected

### Short-term Goals (First Week)

1. **LinkedIn Integration** (Requires Manual Approval):
   - Apply for LinkedIn Developer access
   - Wait for approval (can take 1-2 weeks)
   - Configure OAuth scopes when approved

2. **Fine-tune Automation**:
   - Adjust email notification frequency if needed
   - Review automation thresholds
   - Add custom opportunity criteria

3. **Data Quality**:
   - Verify trade data accuracy
   - Check price arbitrage calculations
   - Review supplier/buyer matching

### Long-term Optimization (First Month)

1. **Performance Monitoring**:
   - Monitor system performance metrics
   - Optimize slow queries/operations
   - Scale hosting resources if needed

2. **Feature Enhancement**:
   - Add custom analytics dashboards
   - Implement advanced filtering
   - Add export functionality

3. **Business Development**:
   - Start using detected opportunities
   - Build supplier/buyer networks
   - Track ROI from platform usage

## 🆘 Getting Help

### Self-Service Resources

1. **Check the logs**:
   - GitHub Actions logs for automation issues
   - Docker logs for local development
   - Email reports for system status

2. **Review configuration**:
   - Verify all GitHub secrets are set
   - Check environment variables
   - Validate email/SMTP settings

3. **Test components individually**:
   - Run MCP server locally
   - Test dashboard independently
   - Verify external API connections

### Support Channels

1. **GitHub Issues**: For bug reports and feature requests
2. **Email Reports**: Automated system status updates
3. **Documentation**: This guide and other docs in the repository

## 📋 Pre-Launch Checklist

Before going live with the platform:

### GitHub Repository Setup
- [ ] All required secrets added to GitHub
- [ ] Email notifications working (test with manual workflow trigger)
- [ ] Docker images building successfully
- [ ] GitHub Actions workflows running without errors

### Local Development
- [ ] Docker Compose working locally
- [ ] Dashboard accessible at http://localhost:8501
- [ ] MCP server responding at http://localhost:8000
- [ ] Email notifications sending locally (optional)

### Cloud Deployment
- [ ] Hosting platform configured (Render/Fly.io/Railway)
- [ ] Services deployed and accessible
- [ ] Environment variables set on hosting platform
- [ ] Domain name configured (optional)

### Integration Testing
- [ ] Automation pipeline running hourly
- [ ] Email reports being received
- [ ] Data sources responding (US Census, World Bank, etc.)
- [ ] Opportunity detection working

### Business Readiness
- [ ] Understanding of detected opportunities
- [ ] Contact process for suppliers/buyers defined
- [ ] Success metrics and KPIs identified
- [ ] LinkedIn approval process initiated

---

**🌍 Ready to dominate Africa-USA trade? Your automated intelligence platform is ready to launch!**

For additional support or questions, check the GitHub repository issues or review the automation email reports for system status updates.