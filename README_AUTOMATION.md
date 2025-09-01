# 🤖 Automated Pipeline Overview - Africa-USA Trade Intelligence Platform

This document explains how the automated pipeline works and provides next steps to supply secrets and finish LinkedIn connector setup.

## 🔄 How the Automation Pipeline Works

The Africa-USA Trade Intelligence Platform now features a comprehensive automation pipeline that runs 24/7 to identify trade opportunities and maintain system health.

### 1. Scheduled Automation (Hourly)

**Workflow**: `.github/workflows/mcp-automation.yml`

Every hour, the system automatically:

1. **🔍 Runs Phase 0 Quick Checks**:
   - Tests MCP server connectivity
   - Verifies memory server availability
   - Checks external data sources (US Census, World Bank, Exchange Rates)
   - Simulates opportunity detection

2. **📊 Generates Intelligence**:
   - Scans for arbitrage opportunities
   - Analyzes market trends
   - Identifies supplier-buyer matches
   - Calculates commission potentials

3. **📧 Sends Email Summary**:
   - System health status
   - Number of opportunities found
   - Data source availability
   - Performance metrics
   - Detailed logs attached

4. **💾 Archives Results**:
   - Uploads scan logs as GitHub artifacts
   - Maintains historical performance data
   - Stores opportunity data for dashboard

### 2. Continuous Deployment (Push-Triggered)

**Workflow**: `.github/workflows/deploy_render.yml`

When code is pushed to main branch:

1. **🐳 Builds Docker Images**:
   - Market Intelligence Server container
   - Streamlit Dashboard container
   - Optimized for production deployment

2. **📤 Pushes to Docker Hub** (if configured):
   - Tagged with commit SHA and branch
   - Cached builds for faster deployments
   - Multi-platform support

3. **🚀 Deploys to Render**:
   - Triggers deployment via Render API
   - Updates both services automatically
   - Zero-downtime deployments

4. **📬 Notifies Success/Failure**:
   - Email notifications for deployment status
   - Links to workflow logs
   - Service health confirmations

### 3. Local Development Stack

**File**: `docker-compose.yml`

For local development and testing:

```bash
# Start full stack
docker-compose up -d

# Services available:
# Dashboard: http://localhost:8501
# Market Intelligence: http://localhost:8000  
# Memory Server: http://localhost:3001
```

## 📋 Architecture Components

### Core Services

1. **Market Intelligence Server** (`Dockerfile.market_intelligence`)
   - MCP server with trade intelligence tools
   - Real-time arbitrage detection
   - API endpoints for dashboard integration
   - Health monitoring and auto-recovery

2. **Streamlit Dashboard** (`Dockerfile.dashboard`)
   - Interactive web interface
   - Real-time opportunity visualization
   - KPI tracking and analytics
   - Mobile-responsive design

3. **Memory Server** (Node.js)
   - Persistent state management
   - Cross-session data storage
   - MCP server memory backend
   - JSON-based lightweight storage

### Automation Scripts

1. **Quick Scan Runner** (`scripts/automation/run_quick_scan.py`)
   - Non-blocking system health checks
   - External API connectivity tests
   - Opportunity detection simulation
   - Performance monitoring

2. **Email Summary Sender** (`scripts/automation/send_email_summary.py`)
   - SMTP-based email notifications (no SendGrid required)
   - HTML and text email formats
   - Log file attachments
   - Error handling and fallbacks

## 🔐 Required Secrets Configuration

### Step 1: Essential Secrets (Start Here)

Add these secrets to GitHub Settings → Secrets and variables → Actions:

```
NOTIFY_EMAIL_TO=your.email@domain.com
NOTIFY_EMAIL_FROM=noreply@yourdomain.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
```

### Step 2: Docker Hub (For Production)

```
DOCKERHUB_USERNAME=your-dockerhub-username
DOCKERHUB_TOKEN=your-dockerhub-access-token
```

### Step 3: Render Deployment (For Cloud Hosting)

```
RENDER_API_KEY=your-render-api-key
RENDER_SERVICE_ID=srv-xxxxxxxxxxxxxx
RENDER_DASHBOARD_SERVICE_ID=srv-xxxxxxxxxxxxxx
```

### Step 4: LinkedIn Integration (Manual Approval Required)

```
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

**⚠️ Note**: LinkedIn API access requires manual approval from LinkedIn. This can take 1-2 weeks.

## 🚀 Getting Started (Quick Setup)

### For Repository Owner (5-Minute Setup)

1. **Add Essential Secrets**:
   ```bash
   # Go to GitHub repo → Settings → Secrets and variables → Actions
   # Add the essential secrets listed above
   ```

2. **Test Automation**:
   ```bash
   # Go to Actions tab → MCP Automation Pipeline → Run workflow
   # Check your email for automation report
   ```

3. **Deploy Locally**:
   ```bash
   git clone https://github.com/trooths2002/africa-usa-trade-intelligence.git
   cd africa-usa-trade-intelligence
   docker-compose up -d
   # Visit http://localhost:8501
   ```

### For Production Deployment

1. **Set up Render hosting** (free tier available)
2. **Configure Docker Hub** for container registry
3. **Add deployment secrets** to GitHub
4. **Push to main branch** → automatic deployment

## 🎯 Next Steps to Complete Setup

### Immediate (Today)

- [ ] **Add GitHub secrets** for email notifications
- [ ] **Test automation pipeline** with manual trigger
- [ ] **Verify email reports** are being received
- [ ] **Run locally** with Docker Compose

### Short-term (This Week)

- [ ] **Set up hosting** on Render or preferred platform
- [ ] **Configure deployment** with Docker Hub integration
- [ ] **Test production deployment** pipeline
- [ ] **Monitor system performance** via email reports

### Medium-term (Next 2 Weeks)

- [ ] **Apply for LinkedIn Developer access**
- [ ] **Configure additional integrations** (Buffer, etc.)
- [ ] **Optimize automation thresholds** based on results
- [ ] **Set up custom domain** (optional)

### Long-term (Next Month)

- [ ] **Complete LinkedIn integration** after approval
- [ ] **Scale hosting resources** based on usage
- [ ] **Add custom analytics** and reporting
- [ ] **Implement advanced features** based on feedback

## 📊 Monitoring and Maintenance

### Automated Monitoring

The system monitors itself and sends reports on:

- **System Health**: All services responding properly
- **Data Quality**: External APIs accessible and returning data
- **Opportunity Detection**: New arbitrage opportunities found
- **Performance Metrics**: Response times, error rates, uptime

### Manual Checks (Weekly)

1. **Review email reports** for trends and issues
2. **Check GitHub Actions** for workflow failures
3. **Monitor hosting platform** usage and performance
4. **Validate opportunity accuracy** and business value

### Scaling Considerations

- **Free tiers** support development and testing
- **Paid tiers** recommended for production traffic
- **Auto-scaling** available on most cloud platforms
- **Database migration** may be needed for high volume

## 🔧 Troubleshooting Common Issues

### Email Notifications Not Working

1. **Check Gmail app password** (not regular password)
2. **Verify 2FA is enabled** on Gmail account
3. **Test SMTP settings** locally first
4. **Check GitHub secrets** are set correctly

### Docker Compose Issues

1. **Update Docker** to latest version
2. **Free up disk space** for container builds
3. **Check port conflicts** (8000, 8501, 3001)
4. **Review container logs** for specific errors

### GitHub Actions Failing

1. **Check workflow logs** in Actions tab
2. **Verify repository secrets** are set
3. **Test locally first** before pushing
4. **Check rate limits** on external APIs

### Deployment Issues

1. **Verify hosting platform** status and limits
2. **Check environment variables** on hosting platform
3. **Review build logs** for dependency issues
4. **Test container locally** before deploying

## 💡 Pro Tips for Success

### Optimization Strategies

1. **Start small**: Use free tiers initially, scale based on results
2. **Monitor closely**: Watch email reports for patterns and issues
3. **Test locally**: Always test changes locally before pushing
4. **Document changes**: Keep track of customizations and settings

### Business Development

1. **Review opportunities daily**: Check email reports for new arbitrage opportunities
2. **Build supplier network**: Use detected opportunities to establish relationships
3. **Track ROI**: Monitor commission earned vs platform costs
4. **Scale gradually**: Increase automation as confidence grows

### Technical Excellence

1. **Keep dependencies updated**: Regular security and performance updates
2. **Monitor resource usage**: Track hosting costs and optimize accordingly  
3. **Backup configurations**: Keep copies of important settings
4. **Plan for growth**: Design for scalability from the start

## 🌍 Vision: Africa-USA Trade Dominance

This automated platform is designed to make you the **#1 Africa-USA agriculture broker** by:

1. **24/7 Opportunity Detection**: Never miss profitable arbitrage opportunities
2. **Automated Intelligence**: Continuous market analysis and supplier discovery
3. **Expert Positioning**: Automated content creation and social media presence
4. **Zero Marginal Cost**: 100% free operation using open-source tools
5. **Scalable Growth**: Infrastructure ready for massive trade volume

### Success Metrics

- **Monthly Revenue**: Track arbitrage opportunities captured
- **Commission Growth**: Monitor brokerage fees earned
- **Network Expansion**: Measure supplier/buyer relationships
- **Market Share**: Assess position in Africa-USA agricultural trade
- **Automation ROI**: Platform cost vs. manual operation savings

---

**🚀 Your automated trade intelligence empire starts now. Add those GitHub secrets and watch the opportunities flow in!**

For detailed setup instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)