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

## Support

For issues or questions, contact the development team or check the documentation.