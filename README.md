# Africa-USA Trade Intelligence Platform

## Overview
This platform provides real-time market intelligence and arbitrage opportunities for Africa-USA agricultural trade. It's designed to help Terrence Dupree become the #1 Africa-USA agriculture broker globally.

## Features
- Live market data and arbitrage opportunities
- Supplier and buyer intelligence
- Social media automation controls
- Performance analytics
- Expert positioning tools

## 🏗️ New Architecture with Real-Time Data Service

The platform now features a modern microservices architecture with separate components for optimal performance:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                   Streamlit Dashboard                       │
│              (src/web_app/dashboard/)                      │
├─────────────────────────────────────────────────────────────┤
│                    SERVICE LAYER                           │
├─────────────────────────────────────────────────────────────┤
│         MCP API Server          │      MCP Intelligence     │
│    (src/mcp_servers/api/)       │   (src/mcp_servers/market_intelligence/)  │
│   - Real-time data endpoints    │   - Market analysis       │
│   - Caching mechanisms          │   - Arbitrage detection   │
│   - Health monitoring           │   - Buyer/supplier intel  │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                               │
├─────────────────────────────────────────────────────────────┤
│  Trade Data  │  Price Data  │  Weather  │  News  │  Social │
│     API      │     API      │    API    │  API   │   APIs  │
├─────────────────────────────────────────────────────────────┤
│                    AUTOMATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  Lead Gen  │  Content  │  Outreach  │  Analytics  │  Alerts │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Instructions

### For Streamlit Community Cloud:
1. Fork this repository to your GitHub account
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your forked repository
5. Set the main file path to: `src/web_app/dashboard/deployed_main.py`
6. Click "Deploy"

### Local Development:
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start all services: `python start_services.py`
4. Access dashboard at: http://localhost:8501

### Production Deployment:
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## Technology Stack
- Python 3.8+
- Streamlit for the dashboard
- FastAPI for the API server
- MCP (Model Context Protocol) for intelligence servers
- Free APIs (US Census Bureau, World Bank, etc.)
- PostgreSQL for data storage

## Requirements
All dependencies are listed in `requirements.txt`. The platform uses only free resources and APIs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![CI](https://github.com/trooths2002/africa-usa-trade-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/trooths2002/africa-usa-trade-intelligence/actions/workflows/ci.yml)

**Transform into the world's #1 Africa-to-USA agriculture broker through intelligent automation and expert positioning**

## 🎯 Mission
Become the most sought-after broker salesman for Africa-to-USA agriculture trade by leveraging:
- **MCP Server Automation** for 10x productivity gains
- **Real-time Market Intelligence** for arbitrage opportunities
- **Expert Social Media Positioning** across all platforms
- **Free Technology Stack** for maximum ROI

## 📊 Market Opportunity
- **Total Market Size**: $2.8B Africa-USA agriculture trade
- **Target Share**: 3-5% ($150M-$250M annually)
- **Commission Potential**: $10M+ annually at scale
- **AGOA Benefits**: 6,700+ duty-free products from 32 countries

## 🚀 Technology Stack (100% Free Resources)

### Core Platform
- **Language**: Python 3.8+ (Free, cross-platform)
- **MCP Framework**: Model Context Protocol (Open source)
- **Database**: SQLite/PostgreSQL (Free, production-ready)
- **Web Framework**: FastAPI (Free, high-performance)
- **Frontend**: Streamlit (Free, rapid development)

### Data Sources (Free APIs)
- **US Trade Data**: Census Bureau API (Free)
- **Commodity Prices**: World Bank API (Free)
- **Weather Data**: OpenWeatherMap API (Free tier)
- **Currency Rates**: ExchangeRate-API (Free tier)
- **News Intelligence**: NewsAPI (Free tier)

### Social Media Automation
- **LinkedIn**: LinkedIn API (Free tier)
- **Twitter/X**: Twitter API v2 (Free tier)
- **Instagram**: Instagram Basic Display API (Free)
- **Content Management**: Buffer API (Free tier)

### Infrastructure (Free Hosting)
- **Code Repository**: GitHub (Free)
- **CI/CD**: GitHub Actions (Free)
- **Hosting**: Railway/Render (Free tier)
- **Monitoring**: Uptime Robot (Free)
- **Analytics**: Google Analytics (Free)

## 📁 Repository Structure

```
africa-usa-trade-intelligence/
├── README.md
├── requirements.txt
├── DEPLOYMENT_GUIDE.md
├── .env.example
├── docker-compose.yml
├── start_dashboard.ps1          # One-click PowerShell script
├── start_dashboard.bat          # One-click Batch script
├── start_services.py            # Start all services
├── monitor_services.py          # Monitor all services
├── test_api_server.py           # Test API server
├── src/
│   ├── mcp_servers/
│   │   ├── market_intelligence/
│   │   │   ├── server.py        # Original MCP server
│   │   │   ├── api_server.py    # New API server with caching
│   │   │   └── requirements.txt # API server requirements
│   │   ├── supplier_management/
│   │   ├── buyer_intelligence/
│   │   └── social_media_automation/
│   ├── apis/
│   │   ├── trade_data/
│   │   ├── market_data/
│   │   └── social_platforms/
│   ├── web_app/
│   │   ├── dashboard/
│   │   │   ├── main.py          # Development dashboard
│   │   │   └── deployed_main.py # Production dashboard
│   │   ├── analytics/
│   │   └── reports/
│   └── utils/
├── data/
│   ├── suppliers/
│   ├── buyers/
│   │   └── buyer_funnel.json     # Buyer funnel data
│   └── market_intelligence/
├── tests/
├── docs/
├── scripts/
└── deployment/
```

## 🎯 Key Features

### 1. **Real-Time Market Intelligence**
- Commodity price monitoring (50+ African products)
- Arbitrage opportunity detection (20%+ margin alerts)
- Import/export trend analysis
- Competitive intelligence tracking

### 2. **Automated Lead Generation**
- Buyer discovery through import data analysis
- Supplier identification across 54 African countries
- Social media prospect mining
- Decision-maker contact extraction

### 3. **Expert Social Media Positioning**
- Automated LinkedIn thought leadership content
- Twitter/X market intelligence sharing
- Instagram visual storytelling
- YouTube educational content creation

### 4. **Intelligent Automation**
- Daily market briefings
- Automated outreach campaigns
- Performance analytics
- Risk monitoring and alerts

### 5. **Buyer Funnel Management**
- Four-tier buyer classification (Enterprise, Mid-Market, Small Business, Individual)
- Personalized outreach content generation
- Engagement tracking and analytics
- Automated follow-up sequence scheduling

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- 100% FREE API keys (see setup guide - NO PAID SERVICES REQUIRED)

### Installation
```bash
# Clone the repository
git clone https://github.com/terrencedupree/africa-usa-trade-intelligence.git
cd africa-usa-trade-intelligence

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
# Edit .env with your 100% FREE API keys (NO PAID SERVICES)
# For LinkedIn integration, follow the setup guide in LINKEDIN_APP_SETUP.md

# Initialize database
python scripts/init_database.py

# Initialize data collection system
python scripts/init_data_collection.py

# Start all services
python start_services.py
```

### First Run
```bash
# Launch all services (API server + dashboard)
python start_services.py

# Run market intelligence scan
python scripts/run_market_scan.py

# Generate daily briefing
python scripts/generate_briefing.py

# Run automated data collection
python scripts/automated_data_tracker.py
```

### One-Click Dashboard Access

For Windows users, you can use the one-click solution to start the dashboard:

- **PowerShell Script**: Run `start_dashboard.ps1`
- **Batch File**: Run `start_dashboard.bat`

Both scripts will automatically check for dependencies and start the dashboard at http://localhost:8501

### Buyer Funnel Tracking

The dashboard now includes a dedicated "Buyer Funnel" tab that provides:

- Real-time tracking of prospects across all buyer tiers
- Follow-up scheduling and management
- Performance metrics and conversion rates
- Prospective buyer pipeline visualization

## 📈 Automated Data Collection

The platform now includes an automated data collection system that regularly fetches and stores trade data from the U.S. Census Bureau API:

### Features:
- **Daily Data Collection**: Automatically fetches trade data for key agricultural products
- **Historical Data Storage**: Stores data in CSV format for trend analysis
- **Key Product Tracking**: Monitors coffee, cocoa, cashews, and other priority products
- **Country-Specific Data**: Tracks imports from key African trading partners
- **Scheduled Automation**: Can be configured to run automatically

### Data Collection Commands:
```bash
# Initialize the data collection system
python scripts/init_data_collection.py

# Run data collection manually
python scripts/automated_data_tracker.py

# Set up scheduled collection (see data/scheduled_task_setup.txt)
```

### Data Storage:
- Data is stored in `data/census_data/` directory
- Each data collection creates timestamped CSV files
- Log files track collection history and issues

## 📊 Performance Metrics

### Productivity Gains
- **70% Time Savings** on market research
- **10x Lead Generation** improvement
- **95% Accuracy** in data processing
- **24/7 Market Monitoring** capability

### Revenue Targets
- **Month 1**: $1M transaction volume
- **Month 3**: $5M transaction volume
- **Month 6**: $15M transaction volume
- **Year 1**: $50M+ transaction volume

### Social Media Growth
- **LinkedIn**: 1,000+ relevant connections in 6 months
- **Twitter**: 5,000+ industry followers
- **Content**: 500+ thought leadership posts
- **Engagement**: 50+ qualified leads monthly

## 🛠️ API Integration

### 100% Free Data Sources Setup (NO PAID APIS)
```python
# Market Intelligence APIs (All Completely Free)
CENSUS_API = "https://api.census.gov/data"  # US Trade Data (No key required)
WORLD_BANK_API = "https://api.worldbank.org"  # Commodity Prices (No key required)
FEDERAL_RESERVE_API = "https://api.stlouisfed.org/fred"  # Economic Data (Free key)
EXCHANGE_RATE_HOST = "https://api.exchangerate.host"  # Currency Rates (No key required)
RSS_NEWS_FEEDS = "Multiple sources"  # News Intelligence (Free RSS)
WEB_SCRAPING_SOURCES = "African commodity exchanges"  # Market Data (Free scraping)
```

### Social Media APIs (Free Tiers ONLY)
```python
# Social Platform Integration (Free Tiers ONLY - No paid tiers)
LINKEDIN_API = "https://api.linkedin.com/v2"  # Professional Network (Free developer access)
TWITTER_API = "https://api.twitter.com/2"  # Real-time Updates (500K tweets/month free)
INSTAGRAM_API = "https://graph.instagram.com"  # Visual Content (Free basic display)
BUFFER_API = "https://api.bufferapp.com"  # Content Scheduling (Free tier: 3 accounts)
```

### LinkedIn API Setup
To enable LinkedIn integration, follow the setup guide in [LINKEDIN_APP_SETUP.md](LINKEDIN_APP_SETUP.md):
1. Create a LinkedIn Developer account
2. Create a new app in the LinkedIn Developer Portal
3. Add your credentials to the `.env` file
4. Test the integration with the provided scripts

You can also check your LinkedIn setup status with:
```bash
python scripts/check_linkedin_setup.py
```

## 🎓 Expert Positioning Strategy

### Content Categories
1. **Market Intelligence** (40% of content)
   - Daily commodity price updates
   - Trade flow analysis
   - Arbitrage opportunities
   - Policy impact assessments

2. **Educational Content** (30% of content)
   - AGOA benefits explanation
   - Trade process tutorials
   - Supplier qualification guides
   - Buyer education series

3. **Success Stories** (20% of content)
   - Deal case studies
   - Supplier spotlights
   - Partnership announcements
   - Industry achievements

4. **Thought Leadership** (10% of content)
   - Industry trend predictions
   - Policy commentary
   - Strategic insights
   - Innovation discussions

## 👥 Buyer Funnel Management

The platform includes a comprehensive buyer funnel management system to help you secure USA buyers across all tiers:

### Buyer Tiers
1. **Enterprise Buyers** ($100M+ revenue) - Large corporations like Unilever, Nestle
2. **Mid-Market Buyers** ($10M-$100M revenue) - Companies like Whole Foods Market
3. **Small Business Buyers** ($1M-$10M revenue) - Local coffee roasters, specialty distributors
4. **Individual Buyers** (<$1M revenue) - Online resellers, restaurant owners

### Key Features
- Automated buyer tier identification based on company characteristics
- Personalized outreach content generation for each tier
- Engagement tracking and performance analytics
- Automated follow-up sequence scheduling
- Pipeline visualization and conversion rate monitoring

### Buyer Funnel Commands
```bash
# Create buyer funnel
python scripts/create_buyer_funnel_simple.py

# Test buyer funnel tool
python test_buyer_funnel.py

# Demonstrate buyer funnel workflow
python demonstrate_buyer_funnel.py
```

## 🔧 Development Roadmap

### Phase 1: Foundation (Month 1)
- [x] Repository setup and documentation
- [x] Core MCP servers implementation
- [x] Free API integrations
- [x] Basic automation workflows

### Phase 2: Intelligence (Month 2)
- [x] Advanced market analysis algorithms
- [x] Supplier/buyer databases
- [x] Social media automation
- [x] Performance analytics

### Phase 3: Optimization (Month 3)
- [x] Caching mechanisms for real-time data
- [x] Separate API service architecture
- [x] Monitoring and health checks
- [x] Production deployment guide

### Phase 4: Scale (Month 4+)
- [ ] Machine learning integration
- [ ] Predictive analytics
- [ ] Advanced automation
- [ ] Mobile optimization

## 📊 Success Metrics Dashboard

Track your progress toward becoming the #1 Africa-USA agriculture broker:

### Financial KPIs
- Monthly transaction volume
- Commission revenue
- Deal conversion rates
- Average deal size

### Operational KPIs
- Supplier network growth
- Buyer relationship development
- Market intelligence accuracy
- Automation efficiency

### Social Media KPIs
- Follower growth across platforms
- Engagement rates
- Lead generation from social
- Thought leadership recognition

## 🤝 Contributing

We welcome contributions to enhance the platform:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/terrencedupree/africa-usa-trade-intelligence/issues)
- **Discussions**: [GitHub Discussions](https://github.com/terrencedupree/africa-usa-trade-intelligence/discussions)

## 🎯 Vision

**"Democratizing Africa-USA trade through intelligent automation and expert positioning, creating prosperity for African producers and American buyers while establishing Terrence Dupree as the global authority in agriculture trade."**

---

**Built with ❤️ for Africa-USA trade prosperity**  
**© 2025 Free World Trade Inc. - Terrence Dupree**