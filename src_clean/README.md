# Africa-USA Trade Intelligence Platform - Clean Architecture

## Overview
This is the clean, simplified architecture for the Africa-USA Trade Intelligence Platform that focuses on:
- Lean, simple, and lightweight implementation
- Intelligent, self-assessing, and self-repairing systems
- $0 cost operation using 100% free resources
- Maximum productivity through MCP servers

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                   Streamlit Dashboard                       │
│                        (dashboard/)                        │
├─────────────────────────────────────────────────────────────┤
│                    SERVICE LAYER                           │
├─────────────────────────────────────────────────────────────┤
│         API Gateway          │      MCP Intelligence        │
│           (api/)             │        (intelligence/)       │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                               │
├─────────────────────────────────────────────────────────────┤
│              Data Collection Service                        │
│                        (data/)                              │
├─────────────────────────────────────────────────────────────┤
│                    MONITORING LAYER                         │
├─────────────────────────────────────────────────────────────┤
│                 Health & Performance                        │
│                      (monitoring/)                          │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Streamlit Dashboard (dashboard/)
- Single, unified dashboard for all intelligence
- Real-time data visualization
- Interactive controls for market analysis

### 2. API Gateway (api/)
- Single entry point for all API requests
- Request routing and load balancing
- Caching layer for performance

### 3. MCP Intelligence Server (intelligence/)
- Market analysis and arbitrage detection
- Buyer/supplier intelligence
- Expert content generation

### 4. Data Collection Service (data/)
- Automated data collection from free APIs
- Data validation and cleaning
- Caching for performance

### 5. Monitoring Service (monitoring/)
- Health checks for all components
- Performance monitoring
- Automated error detection

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start all services:
   ```bash
   python main.py
   ```

3. Access the dashboard at: http://localhost:8501

## Benefits

1. **Simplicity**: Clean, focused architecture with no redundancy
2. **Efficiency**: Intelligent caching and automated processes
3. **Reliability**: Self-monitoring systems
4. **Scalability**: Designed to grow within free tier limits
5. **Maintainability**: Clear structure makes updates easy
6. **Cost-effectiveness**: 100% free operation
7. **Productivity**: MCP servers maximize automation potential