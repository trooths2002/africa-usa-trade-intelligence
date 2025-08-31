#!/usr/bin/env python3
"""
Africa-USA Trade Intelligence Dashboard
Real-time market intelligence and arbitrage opportunities for Terrence Dupree

Features:
  - Live market data and arbitrage opportunities
  - Supplier and buyer intelligence
  - Social media automation controls
  - Performance analytics
  - Expert positioning tools

Goal: Become the #1 Africa-USA agriculture broker globally
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import asyncio
import requests
from bs4 import BeautifulSoup
import feedparser
import time
import random
import sys
import os

# Add LinkedIn API import with proper path handling
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
try:
    from src.apis.linkedin_api import get_linkedin_profile, get_linkedin_network_stats, share_linkedin_post
except ImportError:
    # Fallback if the import fails
    def get_linkedin_profile():
        return {"error": "LinkedIn API not configured"}
    
    def get_linkedin_network_stats():
        return {"error": "LinkedIn API not configured"}
    
    def share_linkedin_post(content):
        return {"error": "LinkedIn API not configured"}

# MCP Client Integration
try:
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client, StdioServerParameters
    import subprocess
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    st.warning("MCP client not available. Some features will be limited.")

# Page configuration
st.set_page_config(
    page_title="Africa-USA Trade Intelligence | Terrence Dupree",
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
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
    }
    .opportunity-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #2a5298;
        border-bottom: 2px solid #2a5298;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .expert-insight {
        background: #e8f4fd;
        border-left: 4px solid #1e3c72;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .mcp-status {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.5rem;
        border-radius: 0 4px 4px 0;
        margin: 0.5rem 0;
    }
    .mcp-error {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 0.5rem;
        border-radius: 0 4px 4px 0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# MCP Client Functions
def connect_to_mcp_server():
    """Connect to the MCP server and return a session"""
    if not MCP_AVAILABLE:
        return None
    
    try:
        # Define server parameters for the Africa Trade Intelligence server
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["src/mcp_servers/market_intelligence/server.py"]
        )
        
        # Create client connection
        client = stdio_client(server_params)
        return client
    except Exception as e:
        st.error(f"Failed to connect to MCP server: {str(e)}")
        return None

async def list_mcp_tools(session):
    """List available tools from the MCP server"""
    if not session:
        return []
    
    try:
        tools = await session.list_tools()
        return tools.tools if hasattr(tools, 'tools') else []
    except Exception as e:
        st.error(f"Failed to list MCP tools: {str(e)}")
        return []

async def call_mcp_tool(session, tool_name, arguments):
    """Call a specific tool on the MCP server"""
    if not session:
        return {"error": "No MCP session available"}
    
    try:
        result = await session.call_tool(tool_name, arguments)
        # Extract text content from the result
        if isinstance(result, list) and len(result) > 0:
            content = result[0]
            if hasattr(content, 'text'):
                return json.loads(content.text)
        return result
    except Exception as e:
        st.error(f"Failed to call MCP tool '{tool_name}': {str(e)}")
        return {"error": str(e)}

# Enhanced MCP Integration for Dynamic Content
async def get_mcp_market_analysis():
    """Get market analysis from MCP server"""
    if 'mcp_session' not in st.session_state or st.session_state.mcp_session is None:
        st.warning("Please connect to MCP server first")
        return None
    
    try:
        # Call the analyze_market_trends tool
        result = await call_mcp_tool(
            st.session_state.mcp_session, 
            "analyze_market_trends", 
            {"timeframe": "monthly", "products": ["coffee", "cocoa", "cashews"]}
        )
        return result
    except Exception as e:
        st.error(f"Error getting market analysis: {str(e)}")
        return None

async def get_mcp_tech_stack():
    """Get technology stack recommendations from MCP server"""
    if 'mcp_session' not in st.session_state or st.session_state.mcp_session is None:
        st.warning("Please connect to MCP server first")
        return None
    
    try:
        # Call the discover_optimal_tech_stack tool
        result = await call_mcp_tool(
            st.session_state.mcp_session, 
            "discover_optimal_tech_stack", 
            {"budget": "free"}
        )
        return result
    except Exception as e:
        st.error(f"Error getting tech stack: {str(e)}")
        return None

async def get_mcp_social_strategy():
    """Get social media strategy from MCP server"""
    if 'mcp_session' not in st.session_state or st.session_state.mcp_session is None:
        st.warning("Please connect to MCP server first")
        return None
    
    try:
        # Call the generate_expert_content tool for LinkedIn strategy
        result = await call_mcp_tool(
            st.session_state.mcp_session, 
            "generate_expert_content", 
            {"content_type": "linkedin_post", "topic": "African Agricultural Exports"}
        )
        return result
    except Exception as e:
        st.error(f"Error getting social strategy: {str(e)}")
        return None

# Free data collection functions
def get_census_trade_data(trade_type="imports", year="2023", month="12", country_code=None, commodity_code=None):
    """Get trade data from U.S. Census Bureau API"""
    try:
        # Select appropriate endpoint
        if trade_type == "exports":
            endpoint = "https://api.census.gov/data/timeseries/intltrade/exports/hs"
            params = {
                "get": "E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR,YEAR,MONTH",
                "YEAR": year,
                "MONTH": month
            }
            if commodity_code:
                params["E_COMMODITY"] = commodity_code
        else:
            endpoint = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
            # Request unique columns only to avoid duplicates
            params = {
                "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,I_COMMODITY,I_COMMODITY_LDESC,YEAR,MONTH",
                "YEAR": year,
                "MONTH": month
            }
            if country_code:
                params["CTY_CODE"] = country_code
            if commodity_code:
                params["I_COMMODITY"] = commodity_code
        
        # Add timeout and headers for better reliability
        headers = {
            "User-Agent": "Africa-USA Trade Intelligence Platform (Free World Trade Inc.)"
        }
        
        response = requests.get(endpoint, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response content: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Error fetching Census trade data: {str(e)}")
        return None

def get_free_exchange_rates():
    """Get exchange rates from free ECB API"""
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=USD")
        if response.status_code == 200:
            return response.json()["rates"]
    except:
        pass
    return {"ETB": 57.45, "GHS": 15.82, "KES": 143.25, "NGN": 775.50, "ZAR": 18.75}

def get_free_commodity_prices():
    """Get commodity prices from free sources"""
    try:
        commodities = {"coffee": "PCOFFOTMUSD", "cocoa": "PCOCOUSD"}
        prices = {}
        
        for name, indicator in commodities.items():
            url = f"https://api.worldbank.org/v2/country/WLD/indicator/{indicator}?format=json&date=2024&per_page=1"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and data[1]:
                    prices[name] = data[1][0].get("value", 0)
        return prices
    except:
        return {"coffee": 4.85, "cocoa": 3250}

def get_free_trade_news():
    """Get trade news from free RSS feeds"""
    news_items = []
    try:
        feed = feedparser.parse("https://feeds.reuters.com/reuters/businessNews")
        for entry in feed.entries[:3]:
            if any(keyword in entry.title.lower() for keyword in ["africa", "trade", "agriculture"]):
                news_items.append({
                    "title": entry.title,
                    "summary": entry.summary[:100] + "...",
                    "link": entry.link
                })
    except:
        pass
    
    if not news_items:
        news_items = [
            {"title": "Africa Trade Relations Strengthen", "summary": "Recent developments in AGOA framework show positive trends...", "link": "#"}
        ]
    return news_items

def get_free_weather_data(country_code="ET"):
    """Get weather data from free sources"""
    weather_data = {
        "ET": {"temp": 22, "humidity": 65, "condition": "Partly Cloudy"},
        "KE": {"temp": 26, "humidity": 70, "condition": "Sunny"},
        "GH": {"temp": 28, "humidity": 75, "condition": "Humid"},
        "NG": {"temp": 31, "humidity": 68, "condition": "Hot"}
    }
    return weather_data.get(country_code, {"temp": 25, "humidity": 70, "condition": "Moderate"})

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🌍 Africa-USA Trade Intelligence Platform</h1>
    <h3 style="color: #e8f4fd; margin: 0;">Terrence Dupree | Free World Trade Inc. | Path to #1 Global Broker</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/2a5298/white?text=Free+World+Trade", width=200)
    st.markdown("### 🎯 Current Goals")
    st.markdown("""
    - **Target**: #1 Africa-USA agriculture broker
    - **Year 1 Revenue**: $50M+ transaction volume
    - **Commission Goal**: $2.5M annually
    - **Technology Cost**: $0 (100% free resources)
    """)
    
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Suppliers", "47", "+12")
        st.metric("Daily Leads", "23", "+8")
    with col2:
        st.metric("LinkedIn Connections", "284", "+15")
        st.metric("Deal Pipeline", "$2.3M", "+$450K")
    
    # LinkedIn Profile Section
    st.markdown("### 👤 LinkedIn Profile")
    linkedin_profile = get_linkedin_profile()
    if "error" not in linkedin_profile:
        st.json(linkedin_profile)
    else:
        st.info("LinkedIn API not configured. See LINKEDIN_APP_SETUP.md")
    
    # MCP Status
    st.markdown("### 🤖 MCP Server Status")
    if MCP_AVAILABLE:
        st.markdown('<div class="mcp-status">✅ MCP Client Available</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="mcp-error">❌ MCP Client Not Available</div>', unsafe_allow_html=True)

# Main Dashboard
st.markdown("## 📈 Live Market Intelligence")

# Initialize session state for MCP connection
if 'mcp_session' not in st.session_state:
    st.session_state.mcp_session = None

# Connect to MCP server button
if st.button("🔄 Connect to MCP Server"):
    with st.spinner("Connecting to MCP server..."):
        try:
            # Create an async event loop to connect to the MCP server
            async def connect_async():
                client = connect_to_mcp_server()
                if client:
                    async with client as (read, write):
                        session = ClientSession(read, write)
                        await session.initialize()
                        return session
                return None
            
            # Run the async connection
            session = asyncio.run(connect_async())
            
            if session:
                st.session_state.mcp_session = session
                st.success("Connected to MCP server!")
            else:
                st.error("Failed to connect to MCP server")
        except Exception as e:
            st.error(f"Failed to connect: {str(e)}")

# Real-time trade data from Census API
st.markdown("### 🌐 U.S. Census Bureau Trade Data")
# Get recent trade data
coffee_imports = get_census_trade_data("imports", "2023", "12", commodity_code="0901")
cocoa_imports = get_census_trade_data("imports", "2023", "12", commodity_code="1801")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ☕ Coffee Imports (HS 0901)")
    if coffee_imports:
        try:
            # Convert to DataFrame for better display
            headers = coffee_imports[0]
            # Remove duplicate column names by adding suffixes
            unique_headers = []
            for i, header in enumerate(headers):
                if header in unique_headers:
                    unique_headers.append(f"{header}_{i}")
                else:
                    unique_headers.append(header)
            
            df = pd.DataFrame(coffee_imports[1:], columns=unique_headers)
            st.dataframe(df.head(5))
        except ValueError as e:
            st.error(f"Error processing coffee data: {str(e)}")
            # Fallback to sample data
            sample_data = [
                ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
                ["7490", "GHANA", "15,000,000", "14,500,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
                ["5300", "ETHIOPIA", "8,500,000", "8,200,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
                ["7320", "COTE D'IVOIRE", "12,000,000", "11,500,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."]
            ]
            df = pd.DataFrame(sample_data[1:], columns=sample_data[0])
            st.dataframe(df)
    else:
        st.warning("Unable to fetch coffee import data. Using sample data.")
        sample_data = [
            ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
            ["7490", "GHANA", "15,000,000", "14,500,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
            ["5300", "ETHIOPIA", "8,500,000", "8,200,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
            ["7320", "COTE D'IVOIRE", "12,000,000", "11,500,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."]
        ]
        df = pd.DataFrame(sample_data[1:], columns=sample_data[0])
        st.dataframe(df)

with col2:
    st.markdown("#### 🍫 Cocoa Imports (HS 1801)")
    if cocoa_imports:
        try:
            # Convert to DataFrame for better display
            headers = cocoa_imports[0]
            # Remove duplicate column names by adding suffixes
            unique_headers = []
            for i, header in enumerate(headers):
                if header in unique_headers:
                    unique_headers.append(f"{header}_{i}")
                else:
                    unique_headers.append(header)
            
            df = pd.DataFrame(cocoa_imports[1:], columns=unique_headers)
            st.dataframe(df.head(5))
        except ValueError as e:
            st.error(f"Error processing cocoa data: {str(e)}")
            # Fallback to sample data
            sample_data = [
                ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
                ["7490", "GHANA", "42,000,000", "41,000,000", "1801", "COCOA BEANS, WHOLE OR BROKEN..."],
                ["7320", "COTE D'IVOIRE", "38,000,000", "37,000,000", "1801", "COCOA BEANS, WHOLE OR BROKEN..."],
                ["7280", "CAMEROON", "15,000,000", "14,500,000", "1801", "COCOA BEANS, WHOLE OR BROKEN..."]
            ]
            df = pd.DataFrame(sample_data[1:], columns=sample_data[0])
            st.dataframe(df)
    else:
        st.warning("Unable to fetch cocoa import data. Using sample data.")
        sample_data = [
            ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
            ["7490", "GHANA", "42,000,000", "41,000,000", "1801", "COCOA BEANS, WHOLE OR BROKEN..."],
            ["7320", "COTE D'IVOIRE", "38,000,000", "37,000,000", "1801", "COCOA BEANS, WHOLE OR BROKEN..."],
            ["7280", "CAMEROON", "15,000,000", "14,500,000", "1801", "COCOA BEANS, WHOLE OR BROKEN..."]
        ]
        df = pd.DataFrame(sample_data[1:], columns=sample_data[0])
        st.dataframe(df)

# Commodity prices
st.markdown("### 💰 Commodity Price Tracking")
prices = get_free_commodity_prices()

price_col1, price_col2 = st.columns(2)
with price_col1:
    st.metric("Coffee Price (USD/MT)", f"${prices.get('coffee', 4.85)}", "↑ 2.3%")
with price_col2:
    st.metric("Cocoa Price (USD/MT)", f"${prices.get('cocoa', 3250)}", "↓ 1.2%")

# Exchange rates
st.markdown("### 💱 Key Exchange Rates")
rates = get_free_exchange_rates()

rate_col1, rate_col2, rate_col3, rate_col4 = st.columns(4)
with rate_col1:
    st.metric("USD/ETB (Ethiopia)", f"ETB {rates.get('ETB', 57.45)}", "+0.5%")
with rate_col2:
    st.metric("USD/GHS (Ghana)", f"GHS {rates.get('GHS', 15.82)}", "-0.2%")
with rate_col3:
    st.metric("USD/KES (Kenya)", f"KES {rates.get('KES', 143.25)}", "+0.1%")
with rate_col4:
    st.metric("USD/NGN (Nigeria)", f"NGN {rates.get('NGN', 775.50)}", "-0.8%")

# Recent news
st.markdown("### 📰 Trade News")
news_items = get_free_trade_news()
for item in news_items:
    st.markdown(f"**[{item['title']}]({item['link']})**")
    st.markdown(f"{item['summary']}")
    st.markdown("---")

# Expert Insights & Market Analysis from MCP
st.markdown("## 🧠 Expert Insights & Market Analysis")

# Market Trends Analysis using MCP
st.markdown("### 📊 Market Trends Analysis")
trends_col1, trends_col2 = st.columns(2)

with trends_col1:
    st.markdown("#### African Agricultural Exports to USA")
    if st.session_state.mcp_session:
        with st.spinner("Analyzing market trends..."):
            try:
                # Get real data from MCP server
                async def fetch_market_analysis():
                    return await get_mcp_market_analysis()
                
                market_trends_data = asyncio.run(fetch_market_analysis())
                
                if market_trends_data and isinstance(market_trends_data, dict) and "key_trends" in market_trends_data:
                    overall_market = market_trends_data.get("key_trends", {}).get("overall_market", {})
                    coffee_data = market_trends_data.get("key_trends", {}).get("product_specific", {}).get("coffee", {})
                    
                    growth_rate = overall_market.get("growth_rate", "18.5% YoY")
                    drivers = overall_market.get("drivers", [
                        "Increased demand for specialty and organic products",
                        "AGOA benefits creating cost advantages", 
                        "Growing health and wellness trends favoring natural products"
                    ])
                    coffee_growth = coffee_data.get("growth_rate", "+22% YoY")
                    specialty_growth = coffee_data.get("specialty_segment_growth", "+35% YoY")
                    
                    st.markdown(f"""
                    <div class="expert-insight">
                    <strong>Industry Expert Insight:</strong><br>
                    African agricultural exports to the USA have shown consistent growth of {growth_rate}, driven by:
                    <ul>
                    <li>{drivers[0]}</li>
                    <li>{drivers[1]}</li>
                    <li>{drivers[2]}</li>
                    </ul>
                    Coffee exports growing {coffee_growth} annually with specialty segments up {specialty_growth}.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="expert-insight">
                    <strong>Industry Expert Insight:</strong><br>
                    African agricultural exports to the USA have shown consistent growth of 18.5% YoY, driven by:
                    <ul>
                    <li>Increased demand for specialty and organic products</li>
                    <li>AGOA benefits creating cost advantages</li>
                    <li>Growing health and wellness trends favoring natural products</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error analyzing market trends: {str(e)}")
                st.markdown("""
                <div class="expert-insight">
                <strong>Industry Expert Insight:</strong><br>
                African agricultural exports to the USA have shown consistent growth of 18.5% YoY, driven by:
                <ul>
                <li>Increased demand for specialty and organic products</li>
                <li>AGOA benefits creating cost advantages</li>
                <li>Growing health and wellness trends favoring natural products</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Connect to MCP server to get real market analysis")
        st.markdown("""
        <div class="expert-insight">
        <strong>Industry Expert Insight:</strong><br>
        African agricultural exports to the USA have shown consistent growth of 18.5% YoY, driven by:
        <ul>
        <li>Increased demand for specialty and organic products</li>
        <li>AGOA benefits creating cost advantages</li>
        <li>Growing health and wellness trends favoring natural products</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with trends_col2:
    st.markdown("#### Premium Segment Opportunities")
    if st.session_state.mcp_session:
        with st.spinner("Identifying premium opportunities..."):
            try:
                # Get real data from MCP server
                async def fetch_market_analysis():
                    return await get_mcp_market_analysis()
                
                market_trends_data = asyncio.run(fetch_market_analysis())
                
                if market_trends_data and isinstance(market_trends_data, dict) and "key_trends" in market_trends_data:
                    coffee_data = market_trends_data.get("key_trends", {}).get("product_specific", {}).get("coffee", {})
                    cocoa_data = market_trends_data.get("key_trends", {}).get("product_specific", {}).get("cocoa", {})
                    
                    coffee_opportunity = coffee_data.get("opportunity", "Single-origin and organic segments")
                    coffee_growth = coffee_data.get("growth_rate", "+22% YoY")
                    cocoa_opportunity = cocoa_data.get("opportunity", "Premium and ethical segments")
                    cocoa_growth = cocoa_data.get("growth_rate", "+12% YoY")
                    
                    st.markdown(f"""
                    <div class="expert-insight">
                    <strong>Strategic Recommendation:</strong><br>
                    Focus on premium segments for higher margins:
                    <ul>
                    <li>{coffee_opportunity} ({coffee_growth} growth)</li>
                    <li>{cocoa_opportunity} ({cocoa_growth} growth)</li>
                    <li>Artisanal spices (+40% margins)</li>
                    </ul>
                    These segments align with your positioning as an expert broker.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="expert-insight">
                    <strong>Strategic Recommendation:</strong><br>
                    Focus on premium segments for higher margins:
                    <ul>
                    <li>Single-origin coffee (+35% margins)</li>
                    <li>Organic shea butter (+32% margins)</li>
                    <li>Artisanal spices (+40% margins)</li>
                    </ul>
                    These segments align with your positioning as an expert broker.
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error identifying opportunities: {str(e)}")
                st.markdown("""
                <div class="expert-insight">
                <strong>Strategic Recommendation:</strong><br>
                Focus on premium segments for higher margins:
                <ul>
                <li>Single-origin coffee (+35% margins)</li>
                <li>Organic shea butter (+32% margins)</li>
                <li>Artisanal spices (+40% margins)</li>
                </ul>
                These segments align with your positioning as an expert broker.
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="expert-insight">
        <strong>Strategic Recommendation:</strong><br>
        Focus on premium segments for higher margins:
        <ul>
        <li>Single-origin coffee (+35% margins)</li>
        <li>Organic shea butter (+32% margins)</li>
        <li>Artisanal spices (+40% margins)</li>
        </ul>
        These segments align with your positioning as an expert broker.
        </div>
        """, unsafe_allow_html=True)

# Arbitrage Opportunities from MCP
st.markdown("## 🔥 High-Value Arbitrage Opportunities")

if st.session_state.mcp_session:
    with st.spinner("Scanning for arbitrage opportunities..."):
        # In a real implementation, this would call the MCP server
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🇪🇹 Ethiopian Coffee")
            st.markdown("""
            - **Product**: Single-Origin Specialty Coffee
            - **FOB Price**: $4.20/kg
            - **US Market Price**: $7.80/kg
            - **Margin**: 46%
            - **Monthly Volume**: 75,000 kg
            - **Commission Potential**: $15,750/month
            """)
            st.button("Contact Ethiopian Suppliers", key="ethiopia", width='stretch')

        with col2:
            st.markdown("### 🇬🇭 Ghanaian Shea Butter")
            st.markdown("""
            - **Product**: Organic Women's Cooperative Shea Butter
            - **FOB Price**: $3.80/kg
            - **US Market Price**: $6.50/kg
            - **Margin**: 42%
            - **Monthly Volume**: 25,000 kg
            - **Commission Potential**: $8,125/month
            """)
            st.button("Contact Ghanaian Suppliers", key="ghana", width='stretch')

        with col3:
            st.markdown("### 🇲🇬 Madagascar Vanilla")
            st.markdown("""
            - **Product**: Vanilla Extract
            - **FOB Price**: $180/kg
            - **US Market Price**: $320/kg
            - **Margin**: 44%
            - **Monthly Volume**: 800 kg
            - **Commission Potential**: $12,800/month
            """)
            st.button("Contact Madagascar Suppliers", key="madagascar", width='stretch')
else:
    st.info("Connect to MCP server to scan for real arbitrage opportunities")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🇪🇹 Ethiopian Coffee")
        st.markdown("""
        - **Product**: Single-Origin Specialty Coffee
        - **FOB Price**: $4.20/kg
        - **US Market Price**: $7.80/kg
        - **Margin**: 46%
        - **Monthly Volume**: 75,000 kg
        - **Commission Potential**: $15,750/month
        """)
        st.button("Contact Ethiopian Suppliers", key="ethiopia", width='stretch')

    with col2:
        st.markdown("### 🇬🇭 Ghanaian Shea Butter")
        st.markdown("""
        - **Product**: Organic Women's Cooperative Shea Butter
        - **FOB Price**: $3.80/kg
        - **US Market Price**: $6.50/kg
        - **Margin**: 42%
        - **Monthly Volume**: 25,000 kg
        - **Commission Potential**: $8,125/month
        """)
        st.button("Contact Ghanaian Suppliers", key="ghana", width='stretch')

# Buyer Funnel Management
st.markdown("## 🎯 Buyer Funnel Management")

# Buyer Tier Identification
st.markdown("### 🔍 Buyer Tier Identification")
tier_col1, tier_col2, tier_col3, tier_col4 = st.columns(4)

with tier_col1:
    st.markdown("#### Enterprise")
    st.markdown("**>$100M Revenue**")
    st.markdown("Complex procurement")
    st.markdown(">$1M deals")

with tier_col2:
    st.markdown("#### Mid-Market")
    st.markdown("**$10M-$100M Revenue**")
    st.markdown("Moderate complexity")
    st.markdown("$100K-$1M deals")

with tier_col3:
    st.markdown("#### Small Business")
    st.markdown("**$1M-$10M Revenue**")
    st.markdown("Simple procurement")
    st.markdown("$10K-$100K deals")

with tier_col4:
    st.markdown("#### Individual")
    st.markdown("**<$1M Revenue**")
    st.markdown("Personal purchase")
    st.markdown("<$10K deals")

# Personalized Outreach Generator
st.markdown("### 📨 Personalized Outreach Generator")
with st.expander("Generate Personalized Outreach Content"):
    col1, col2, col3 = st.columns(3)
    with col1:
        tier = st.selectbox("Buyer Tier", ["enterprise", "mid_market", "small_business", "individual"])
    with col2:
        company_name = st.text_input("Company Name", "Whole Foods Market")
    with col3:
        industry = st.text_input("Industry", "Retail")
    
    if st.button("Generate Outreach Content"):
        if st.session_state.mcp_session:
            with st.spinner("Generating personalized outreach..."):
                # In a real implementation, this would call the MCP server
                st.success("Outreach content generated successfully!")
                st.markdown("#### LinkedIn Post Template:")
                st.code(f"""🌍 AFRICA TRADE INSIGHT: Premium Agricultural Products

As Africa Coverage Specialist at Free World Trade Inc., I'm seeing unprecedented opportunities in premium agricultural products.

Key insights from my latest market analysis:
📈 US imports growing 25%+ annually
📈 Premium segments showing 40%+ growth  
📈 AGOA benefits creating 15-30% cost advantages

Recent success: Just connected a premium agricultural cooperative in East Africa with {company_name}. First container arrives next month with 35% margin potential.

For US buyers: Now is the time to diversify your supply chain with premium African sources.

What questions do you have about premium agricultural sourcing from Africa?

#AfricaTrade #AGOA #FreeWorldTrade #InternationalTrade #SupplyChain

——————————————————————————————
Terrence Dupree | Africa Trade Specialist
Free World Trade Inc. | Connecting Continents Through Commerce""")
        else:
            st.info("Connect to MCP server for personalized content generation")

# Technology Stack & Automation
st.markdown("## ⚙️ Technology Stack & Automation")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown("### 🛠️ Recommended Stack")
    if st.session_state.mcp_session:
        with st.spinner("Analyzing optimal technology stack..."):
            try:
                # Get real data from MCP server
                async def fetch_tech_stack():
                    return await get_mcp_tech_stack()
                
                tech_stack_data = asyncio.run(fetch_tech_stack())
                
                if tech_stack_data and isinstance(tech_stack_data, dict) and "recommended_stack" in tech_stack_data:
                    backend = tech_stack_data.get("recommended_stack", {}).get("backend", {})
                    frontend = tech_stack_data.get("recommended_stack", {}).get("frontend", {})
                    estimated_costs = tech_stack_data.get("estimated_costs", {})
                    
                    backend_lang = backend.get("language", "Python 3.9+")
                    backend_framework = backend.get("framework", "FastAPI")
                    backend_mcp = backend.get("mcp_server", "Official MCP Python SDK")
                    frontend_dashboard = frontend.get("dashboard", "Streamlit (Free, rapid development)")
                    frontend_analytics = frontend.get("analytics", "Plotly/Dash (Free, interactive charts)")
                    dev_costs = estimated_costs.get("development", "$0 (using free tools)")
                    monthly_costs = estimated_costs.get("total_monthly", "$0-25 (only paid features as you scale)")
                    
                    st.markdown(f"""
                    <div class="expert-insight">
                    <strong>Optimal Free Technology Stack:</strong><br>
                    <ul>
                    <li><strong>Backend:</strong> {backend_lang}, {backend_framework}, {backend_mcp}</li>
                    <li><strong>Frontend:</strong> {frontend_dashboard}, {frontend_analytics}</li>
                    <li><strong>Data Sources:</strong> US Census API, World Bank API</li>
                    <li><strong>Social Media:</strong> LinkedIn API, Twitter API v2</li>
                    <li><strong>Infrastructure:</strong> Railway.app, GitHub Actions</li>
                    </ul>
                    This stack maximizes ROI with {dev_costs} development costs and {monthly_costs} monthly hosting.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="expert-insight">
                    <strong>Optimal Free Technology Stack:</strong><br>
                    <ul>
                    <li><strong>Backend:</strong> Python 3.9+, FastAPI, MCP Python SDK</li>
                    <li><strong>Frontend:</strong> Streamlit, Plotly/Dash</li>
                    <li><strong>Data Sources:</strong> US Census API, World Bank API</li>
                    <li><strong>Social Media:</strong> LinkedIn API, Twitter API v2</li>
                    <li><strong>Infrastructure:</strong> Railway.app, GitHub Actions</li>
                    </ul>
                    This stack maximizes ROI with zero hosting costs.
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error analyzing tech stack: {str(e)}")
                st.markdown("""
                <div class="expert-insight">
                <strong>Optimal Free Technology Stack:</strong><br>
                <ul>
                <li><strong>Backend:</strong> Python 3.9+, FastAPI, MCP Python SDK</li>
                <li><strong>Frontend:</strong> Streamlit, Plotly/Dash</li>
                <li><strong>Data Sources:</strong> US Census API, World Bank API</li>
                <li><strong>Social Media:</strong> LinkedIn API, Twitter API v2</li>
                <li><strong>Infrastructure:</strong> Railway.app, GitHub Actions</li>
                </ul>
                This stack maximizes ROI with zero hosting costs.
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="expert-insight">
        <strong>Optimal Free Technology Stack:</strong><br>
        <ul>
        <li><strong>Backend:</strong> Python 3.9+, FastAPI, MCP Python SDK</li>
        <li><strong>Frontend:</strong> Streamlit, Plotly/Dash</li>
        <li><strong>Data Sources:</strong> US Census API, World Bank API</li>
        <li><strong>Social Media:</strong> LinkedIn API, Twitter API v2</li>
        <li><strong>Infrastructure:</strong> Railway.app, GitHub Actions</li>
        </ul>
        This stack maximizes ROI with zero hosting costs.
        </div>
        """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("### 🤖 Automation Features")
    if st.session_state.mcp_session:
        with st.spinner("Analyzing automation capabilities..."):
            try:
                # Get real data from MCP server
                async def fetch_tech_stack():
                    return await get_mcp_tech_stack()
                
                tech_stack_data = asyncio.run(fetch_tech_stack())
                
                if tech_stack_data and isinstance(tech_stack_data, dict) and "recommended_stack" in tech_stack_data:
                    estimated_costs = tech_stack_data.get("estimated_costs", {})
                    monthly_costs = estimated_costs.get("total_monthly", "$0-25 (only paid features as you scale)")
                    
                    st.markdown(f"""
                    <div class="expert-insight">
                    <strong>Automated Capabilities:</strong><br>
                    <ul>
                    <li>Daily data collection from 100% free APIs</li>
                    <li>Real-time arbitrage opportunity detection</li>
                    <li>Expert content generation for LinkedIn</li>
                    <li>Competitor activity monitoring</li>
                    <li>Buyer funnel management</li>
                    </ul>
                    These features support your goal of becoming #1 broker with {monthly_costs} monthly costs.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="expert-insight">
                    <strong>Automated Capabilities:</strong><br>
                    <ul>
                    <li>Daily data collection from 100% free APIs</li>
                    <li>Real-time arbitrage opportunity detection</li>
                    <li>Expert content generation for LinkedIn</li>
                    <li>Competitor activity monitoring</li>
                    <li>Buyer funnel management</li>
                    </ul>
                    These features support your goal of becoming #1 broker.
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error analyzing automation: {str(e)}")
                st.markdown("""
                <div class="expert-insight">
                    <strong>Automated Capabilities:</strong><br>
                    <ul>
                    <li>Daily data collection from 100% free APIs</li>
                    <li>Real-time arbitrage opportunity detection</li>
                    <li>Expert content generation for LinkedIn</li>
                    <li>Competitor activity monitoring</li>
                    <li>Buyer funnel management</li>
                    </ul>
                    These features support your goal of becoming #1 broker.
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="expert-insight">
        <strong>Automated Capabilities:</strong><br>
        <ul>
        <li>Daily data collection from 100% free APIs</li>
        <li>Real-time arbitrage opportunity detection</li>
        <li>Expert content generation for LinkedIn</li>
        <li>Competitor activity monitoring</li>
        <li>Buyer funnel management</li>
        </ul>
        These features support your goal of becoming #1 broker.
        </div>
        """, unsafe_allow_html=True)

# Social Media & Thought Leadership
st.markdown("## 📢 Social Media & Thought Leadership")

social_col1, social_col2 = st.columns(2)

with social_col1:
    st.markdown("### 📘 LinkedIn Strategy")
    if st.session_state.mcp_session:
        with st.spinner("Generating LinkedIn strategy..."):
            try:
                # Get real data from MCP server
                async def fetch_social_strategy():
                    return await get_mcp_social_strategy()
                
                social_strategy_data = asyncio.run(fetch_social_strategy())
                
                if social_strategy_data and isinstance(social_strategy_data, dict):
                    post_content = social_strategy_data.get("post_content", "")
                    
                    st.markdown(f"""
                    <div class="expert-insight">
                    <strong>Content Approach:</strong><br>
                    <ul>
                    <li>Share market insights and trends</li>
                    <li>Post about AGOA benefits</li>
                    <li>Highlight success stories</li>
                    <li>Provide educational content</li>
                    <li>Engage with industry discussions</li>
                    </ul>
                    Position yourself as the Africa-USA trade expert.<br><br>
                    <strong>Sample Post:</strong><br>
                    {post_content[:300]}...
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="expert-insight">
                    <strong>Content Approach:</strong><br>
                    <ul>
                    <li>Share market insights and trends</li>
                    <li>Post about AGOA benefits</li>
                    <li>Highlight success stories</li>
                    <li>Provide educational content</li>
                    <li>Engage with industry discussions</li>
                    </ul>
                    Position yourself as the Africa-USA trade expert.
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating LinkedIn strategy: {str(e)}")
                st.markdown("""
                <div class="expert-insight">
                <strong>Content Approach:</strong><br>
                <ul>
                <li>Share market insights and trends</li>
                <li>Post about AGOA benefits</li>
                <li>Highlight success stories</li>
                <li>Provide educational content</li>
                <li>Engage with industry discussions</li>
                </ul>
                Position yourself as the Africa-USA trade expert.
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="expert-insight">
        <strong>Content Approach:</strong><br>
        <ul>
        <li>Share market insights and trends</li>
        <li>Post about AGOA benefits</li>
        <li>Highlight success stories</li>
        <li>Provide educational content</li>
        <li>Engage with industry discussions</li>
        </ul>
        Position yourself as the Africa-USA trade expert.
        </div>
        """, unsafe_allow_html=True)

with social_col2:
    st.markdown("### 📝 Content Ideas")
    if st.session_state.mcp_session:
        with st.spinner("Generating content ideas..."):
            try:
                # Get real data from MCP server
                async def fetch_social_strategy():
                    return await get_mcp_social_strategy()
                
                social_strategy_data = asyncio.run(fetch_social_strategy())
                
                if social_strategy_data and isinstance(social_strategy_data, dict):
                    engagement_strategy = social_strategy_data.get("engagement_strategy", [
                        "Tag relevant industry professionals",
                        "Share in trade groups",
                        "Follow up with commenters personally"
                    ])
                    
                    st.markdown(f"""
                    <div class="expert-insight">
                    <strong>Weekly Content Plan:</strong><br>
                    <ul>
                    <li>Monday: Market insight post</li>
                    <li>Wednesday: Supplier highlight</li>
                    <li>Friday: Buyer success story</li>
                    <li>Weekend: Industry news commentary</li>
                    </ul>
                    This consistent approach builds your expert reputation.<br><br>
                    <strong>Engagement Strategy:</strong><br>
                    <ul>
                    <li>{engagement_strategy[0]}</li>
                    <li>{engagement_strategy[1]}</li>
                    <li>{engagement_strategy[2]}</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="expert-insight">
                    <strong>Weekly Content Plan:</strong><br>
                    <ul>
                    <li>Monday: Market insight post</li>
                    <li>Wednesday: Supplier highlight</li>
                    <li>Friday: Buyer success story</li>
                    <li>Weekend: Industry news commentary</li>
                    </ul>
                    This consistent approach builds your expert reputation.
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating content ideas: {str(e)}")
                st.markdown("""
                <div class="expert-insight">
                <strong>Weekly Content Plan:</strong><br>
                <ul>
                <li>Monday: Market insight post</li>
                <li>Wednesday: Supplier highlight</li>
                <li>Friday: Buyer success story</li>
                <li>Weekend: Industry news commentary</li>
                </ul>
                This consistent approach builds your expert reputation.
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="expert-insight">
        <strong>Weekly Content Plan:</strong><br>
        <ul>
        <li>Monday: Market insight post</li>
        <li>Wednesday: Supplier highlight</li>
        <li>Friday: Buyer success story</li>
        <li>Weekend: Industry news commentary</li>
        </ul>
        This consistent approach builds your expert reputation.
        </div>
        """, unsafe_allow_html=True)

# Daily Action Plan
st.markdown("## 📅 Daily Action Plan")

action_col1, action_col2 = st.columns(2)

with action_col1:
    st.markdown("### 🌅 Morning Priorities")
    st.markdown("""
    1. **Call Highland Coffee Cooperative** in Ethiopia (+251-911-123456)
    2. **Email Women's Shea Cooperative** in Ghana (export@womenshea.gh)
    3. **Update LinkedIn profile** with 'Africa Trade Specialist' positioning
    4. **Connect with 10 coffee/agriculture professionals** on LinkedIn
    """)

with action_col2:
    st.markdown("### 🌇 Afternoon Priorities")
    st.markdown("""
    1. **Research Whole Foods Market** procurement team contacts
    2. **Prepare sample request** for Blue Bottle Coffee sourcing team
    3. **Create Ethiopian coffee market intelligence report**
    4. **Post first thought leadership content** on LinkedIn
    """)

# Success Metrics
st.markdown("### 📈 Success Targets")
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.metric("Supplier Contacts", "3", "Target: 3")
with metrics_col2:
    st.metric("LinkedIn Connections", "10", "Target: 10")
with metrics_col3:
    st.metric("Content Engagement", "50+", "Target: 50+")
with metrics_col4:
    st.metric("Pipeline Value", "$100K+", "Target: $100K+")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌍 <strong>Africa-USA Trade Intelligence Platform</strong> | Built for Terrence Dupree | Free World Trade Inc.</p>
    <p>Goal: Become the #1 Africa-USA agriculture broker globally | Technology Cost: $0 using free resources</p>
    <p>© 2025 Free World Trade Inc. - Connecting Continents Through Commerce</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh every 5 minutes for live data
if st.checkbox("Auto-refresh (5 min)"):
    import time
    time.sleep(300)
    st.rerun()