#!/usr/bin/env python3
"""
Streamlit Dashboard Stub for Africa-USA Trade Intelligence Platform
A comprehensive dashboard connecting to MCP server or using sample data

This is a stub implementation that:
1. Attempts to connect to the local FastAPI proxy or MCP server directly
2. Falls back to sample JSON data if MCP server is not reachable
3. Provides placeholder sections for further development
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import requests
import os
import sys
from typing import Dict, Any, Optional

# Add the current directory to the path to help with imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Africa-USA Trade Intelligence | Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2a5298;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .opportunity-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .status-indicator {
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-online { background-color: #d4edda; color: #155724; }
    .status-offline { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# Configuration
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
MEMORY_SERVER_URL = os.getenv('MEMORY_SERVER_URL', 'http://localhost:3001')

def check_mcp_server_connection() -> bool:
    """Check if MCP server is reachable"""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        # Try alternative endpoint
        try:
            response = requests.get(f"{MCP_SERVER_URL}/", timeout=5)
            return response.status_code == 200
        except:
            return False

def load_sample_data() -> Dict[str, Any]:
    """Load sample data for demonstration when MCP server is not available"""
    return {
        "overview_kpis": {
            "active_opportunities": 12,
            "monthly_revenue_potential": 850000,
            "commission_potential": 127500,
            "active_suppliers": 34,
            "active_buyers": 28,
            "conversion_rate": 23.5
        },
        "live_opportunities": [
            {
                "id": 1,
                "product": "Premium Cashews",
                "origin_country": "Ghana",
                "destination": "New York, USA",
                "price_arbitrage": 45.2,
                "commission_potential": 35000,
                "urgency": "High",
                "agoa_eligible": True,
                "contact_supplier": "Kwame Enterprises Ltd.",
                "contact_buyer": "Atlantic Nuts Trading Co.",
                "last_updated": "2025-01-01 10:30:00"
            },
            {
                "id": 2,
                "product": "Organic Shea Butter",
                "origin_country": "Burkina Faso",
                "destination": "California, USA", 
                "price_arbitrage": 38.7,
                "commission_potential": 28500,
                "urgency": "Medium",
                "agoa_eligible": True,
                "contact_supplier": "Burkina Bio Products",
                "contact_buyer": "Natural Beauty Supply Inc.",
                "last_updated": "2025-01-01 09:45:00"
            },
            {
                "id": 3,
                "product": "Premium Coffee Beans",
                "origin_country": "Ethiopia",
                "destination": "Seattle, USA",
                "price_arbitrage": 52.1,
                "commission_potential": 42000,
                "urgency": "High",
                "agoa_eligible": True,
                "contact_supplier": "Ethiopian Highland Coffee",
                "contact_buyer": "Pacific Coffee Roasters",
                "last_updated": "2025-01-01 11:15:00"
            }
        ],
        "market_trends": {
            "top_products": ["Cashews", "Coffee", "Shea Butter", "Vanilla", "Spices"],
            "growth_rates": [12.5, 18.3, 15.7, 22.1, 9.8],
            "market_size": [450000, 680000, 320000, 180000, 240000]
        }
    }

def fetch_mcp_data() -> Optional[Dict[str, Any]]:
    """Attempt to fetch data from MCP server"""
    try:
        # Try to connect to MCP server via different methods
        
        # Method 1: Direct MCP client connection (if available)
        try:
            # This would use mcp_python_client if available
            # For now, we'll simulate the connection
            pass
        except ImportError:
            pass
        
        # Method 2: HTTP API connection
        response = requests.get(f"{MCP_SERVER_URL}/market_analysis", timeout=10)
        if response.status_code == 200:
            return response.json()
            
        # Method 3: SSE endpoint
        response = requests.get(f"{MCP_SERVER_URL}/sse/market_data", timeout=10)
        if response.status_code == 200:
            return response.json()
            
    except Exception as e:
        st.sidebar.warning(f"MCP Connection Error: {str(e)}")
    
    return None

# Header
st.markdown("""
<div class="main-header">
    <h1>🌍 Africa-USA Trade Intelligence Dashboard</h1>
    <p>Real-time market intelligence for strategic trade opportunities</p>
</div>
""", unsafe_allow_html=True)

# Server Status Check
is_mcp_online = check_mcp_server_connection()

# Sidebar
with st.sidebar:
    st.title("📊 Dashboard Controls")
    
    # Server Status
    status_class = "status-online" if is_mcp_online else "status-offline"
    status_text = "🟢 Online" if is_mcp_online else "🔴 Offline (Using Sample Data)"
    
    st.markdown(f"""
    <div class="status-indicator {status_class}">
        MCP Server: {status_text}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Refresh Controls
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    if auto_refresh:
        st.info("Auto-refresh enabled")
        # Note: In production, implement proper auto-refresh with st.rerun()
    
    st.markdown("---")
    
    # Filters
    st.subheader("🔍 Filters")
    selected_countries = st.multiselect(
        "Origin Countries",
        ["Ghana", "Nigeria", "Kenya", "Ethiopia", "Burkina Faso", "Côte d'Ivoire"],
        default=["Ghana", "Ethiopia"]
    )
    
    min_commission = st.slider(
        "Minimum Commission ($)",
        min_value=1000,
        max_value=100000,
        value=20000,
        step=5000
    )

# Load Data
if is_mcp_online:
    data = fetch_mcp_data()
    if data is None:
        st.warning("⚠️ MCP server is online but returned no data. Using sample data.")
        data = load_sample_data()
else:
    data = load_sample_data()
    st.info("📝 Using sample data - MCP server connection not available")

# Main Dashboard Content
col1, col2, col3 = st.columns(3)

# Overview KPIs
kpis = data.get("overview_kpis", {})

with col1:
    st.metric(
        "💰 Revenue Potential", 
        f"${kpis.get('monthly_revenue_potential', 0):,.0f}",
        delta="12.5%"
    )
    st.metric(
        "🎯 Active Opportunities", 
        kpis.get('active_opportunities', 0),
        delta="3"
    )

with col2:
    st.metric(
        "💵 Commission Potential", 
        f"${kpis.get('commission_potential', 0):,.0f}",
        delta="8.2%"
    )
    st.metric(
        "📈 Conversion Rate", 
        f"{kpis.get('conversion_rate', 0):.1f}%",
        delta="2.1%"
    )

with col3:
    st.metric(
        "🏭 Active Suppliers", 
        kpis.get('active_suppliers', 0),
        delta="5"
    )
    st.metric(
        "🏢 Active Buyers", 
        kpis.get('active_buyers', 0),
        delta="2"
    )

st.markdown("---")

# Live Opportunities Table
st.subheader("🔥 Live Opportunities")

opportunities = data.get("live_opportunities", [])

if opportunities:
    # Filter opportunities based on sidebar selections
    filtered_opportunities = [
        opp for opp in opportunities
        if opp.get("origin_country") in selected_countries
        and opp.get("commission_potential", 0) >= min_commission
    ]
    
    if filtered_opportunities:
        df = pd.DataFrame(filtered_opportunities)
        
        # Format the dataframe for display
        display_df = df[['product', 'origin_country', 'destination', 'price_arbitrage', 
                        'commission_potential', 'urgency', 'agoa_eligible', 'last_updated']].copy()
        
        display_df.columns = ['Product', 'Origin', 'Destination', 'Arbitrage %', 
                             'Commission $', 'Urgency', 'AGOA Eligible', 'Last Updated']
        
        # Format numeric columns
        display_df['Commission $'] = display_df['Commission $'].apply(lambda x: f"${x:,.0f}")
        display_df['Arbitrage %'] = display_df['Arbitrage %'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Urgency": st.column_config.SelectboxColumn(
                    options=["Low", "Medium", "High"]
                ),
                "AGOA Eligible": st.column_config.CheckboxColumn()
            }
        )
        
        # Detailed opportunity cards
        st.subheader("📋 Opportunity Details")
        
        for opp in filtered_opportunities[:3]:  # Show top 3
            with st.expander(f"🎯 {opp['product']} - ${opp['commission_potential']:,.0f} commission"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write(f"**Origin:** {opp['origin_country']}")
                    st.write(f"**Destination:** {opp['destination']}")
                    st.write(f"**Price Arbitrage:** {opp['price_arbitrage']:.1f}%")
                    st.write(f"**AGOA Eligible:** {'✅ Yes' if opp['agoa_eligible'] else '❌ No'}")
                
                with col_b:
                    st.write(f"**Supplier:** {opp['contact_supplier']}")
                    st.write(f"**Buyer:** {opp['contact_buyer']}")
                    st.write(f"**Urgency:** {opp['urgency']}")
                    st.write(f"**Last Updated:** {opp['last_updated']}")
                
                if st.button(f"🚀 Initiate Contact for {opp['product']}", key=f"contact_{opp['id']}"):
                    st.success("Contact initiation logged! 📧 Email notifications will be sent to both parties.")
    
    else:
        st.warning("No opportunities match the current filters. Please adjust your criteria.")

else:
    st.error("No opportunities data available")

st.markdown("---")

# Market Trends Visualization
if "market_trends" in data:
    st.subheader("📈 Market Trends")
    
    trends = data["market_trends"]
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Top Products by Growth Rate
        fig_growth = px.bar(
            x=trends["top_products"],
            y=trends["growth_rates"],
            title="Growth Rate by Product Category",
            labels={"x": "Product", "y": "Growth Rate (%)"}
        )
        fig_growth.update_layout(showlegend=False)
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col_chart2:
        # Market Size Distribution
        fig_size = px.pie(
            values=trends["market_size"],
            names=trends["top_products"],
            title="Market Size Distribution ($)"
        )
        st.plotly_chart(fig_size, use_container_width=True)

st.markdown("---")

# Development Instructions
st.subheader("🚧 Development Instructions")

with st.expander("📝 How to Extend This Dashboard"):
    st.markdown("""
    ### Next Steps for Development:
    
    1. **MCP Client Integration**
       - Install `mcp_python_client` package
       - Implement proper MCP client connection in `fetch_mcp_data()`
       - Add error handling and retry logic
    
    2. **Real-time Data Connection**
       - Connect to live FastAPI proxy at `http://localhost:8000`
       - Implement SSE (Server-Sent Events) for real-time updates
       - Add WebSocket support for bidirectional communication
    
    3. **Enhanced Features to Add**
       - Interactive charts with drill-down capabilities
       - Email notification system for new opportunities
       - Export functionality (PDF, Excel)
       - User authentication and role-based access
       - Mobile-responsive design improvements
    
    4. **Data Sources Integration**
       - US Census Bureau trade data
       - World Bank commodity prices
       - Exchange rate feeds
       - News and market sentiment analysis
    
    5. **Performance Optimizations**
       - Implement data caching with Redis
       - Add database connection pooling
       - Optimize chart rendering for large datasets
       - Add lazy loading for historical data
    
    ### Configuration Required:
    - Set environment variables: `MCP_SERVER_URL`, `MEMORY_SERVER_URL`
    - Configure API keys in `.env` file
    - Set up database connections
    - Configure email SMTP settings
    """)

with st.expander("⚙️ Environment Variables"):
    st.code("""
# Required Environment Variables
MCP_SERVER_URL=http://localhost:8000
MEMORY_SERVER_URL=http://localhost:3001
DATABASE_URL=postgresql://user:pass@localhost/db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@domain.com
SMTP_PASSWORD=your_app_password
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
BUFFER_API_KEY=your_buffer_api_key
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🌍 Africa-USA Trade Intelligence Platform | Built with ❤️ for global trade</p>
    <p>Dashboard Status: {status} | Last Updated: {timestamp}</p>
</div>
""".format(
    status="🟢 Connected" if is_mcp_online else "🟡 Sample Data Mode",
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
), unsafe_allow_html=True)

# Auto-refresh logic (if enabled)
if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()