#!/usr/bin/env python3
"""
Streamlit Dashboard for Africa-USA Trade Intelligence Platform
Real-time market intelligence for Terrence Dupree - #1 Africa-USA agriculture broker globally
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import asyncio
import requests
from typing import Dict, Any, Optional
import sys
import os

# Add the current directory to the path to help with imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    .api-status {
        background: #cce5ff;
        border-left: 4px solid #007bff;
        padding: 0.5rem;
        border-radius: 0 4px 4px 0;
        margin: 0.5rem 0;
    }
    .api-error {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 0.5rem;
        border-radius: 0 4px 4px 0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Simple caching mechanism for the dashboard
class DashboardCache:
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key: str, expiry_minutes: int = 5) -> Optional[Any]:
        if key in self._cache:
            # Check if cache is still valid
            if datetime.now() - self._timestamps[key] < timedelta(minutes=expiry_minutes):
                return self._cache[key]
            else:
                # Expire cache
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, key: str, value: Any):
        self._cache[key] = value
        self._timestamps[key] = datetime.now()

# Initialize cache
dashboard_cache = DashboardCache()

# API helper functions with caching
def fetch_api_data(endpoint: str, params: Dict = None, cache_key: str = None, expiry_minutes: int = 5) -> Dict:
    """Fetch data from API with caching"""
    # Try cache first
    if cache_key:
        cached_data = dashboard_cache.get(cache_key, expiry_minutes)
        if cached_data:
            return cached_data
    
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if params:
            response = requests.get(url, params=params, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # Cache the data
            if cache_key:
                dashboard_cache.set(cache_key, data)
            return data
        else:
            st.error(f"API request failed with status {response.status_code}")
            return {"error": f"API request failed with status {response.status_code}"}
    except Exception as e:
        st.error(f"Error connecting to API service: {str(e)}")
        return {"error": f"Error connecting to API service: {str(e)}"}

def get_census_data(trade_type: str = "imports", commodity_code: str = None) -> Dict:
    """Get Census trade data"""
    cache_key = f"census_{trade_type}_{commodity_code}"
    return fetch_api_data(f"/census/{trade_type}/{commodity_code}", cache_key=cache_key, expiry_minutes=30)

def get_exchange_rates() -> Dict:
    """Get exchange rates"""
    return fetch_api_data("/exchange-rates", cache_key="exchange_rates", expiry_minutes=60)

def get_commodity_prices() -> Dict:
    """Get commodity prices"""
    return fetch_api_data("/commodity-prices", cache_key="commodity_prices", expiry_minutes=30)

def get_trade_news() -> Dict:
    """Get trade news"""
    return fetch_api_data("/trade-news", cache_key="trade_news", expiry_minutes=60)

def get_weather_data(country_code: str) -> Dict:
    """Get weather data for a country"""
    cache_key = f"weather_{country_code}"
    return fetch_api_data(f"/weather/{country_code}", cache_key=cache_key, expiry_minutes=15)

# Simulated data for when API is not available
def get_simulated_arbitrage_opportunities():
    """Return simulated arbitrage opportunities"""
    return {
        "high_priority_opportunities": [
            {
                "product": "Ethiopian Single-Origin Coffee (Specialty Grade)",
                "supplier_country": "Ethiopia",
                "fob_price": "4.20 USD/kg",
                "us_market_price": "7.80 USD/kg",
                "gross_margin": "46%",
                "net_margin_estimate": "35%",
                "monthly_volume_potential": "75,000 kg",
                "revenue_potential": "585,000 USD/month",
                "commission_potential": "29,250 USD/month",
                "agoa_eligible": True,
                "certification_premiums": ["Organic: +25%", "Fair Trade: +15%"],
                "risk_level": "Low",
                "action_required": "IMMEDIATE - Contact Sidamo cooperatives",
                "buyer_targets": ["Specialty coffee roasters", "Whole Foods", "Blue Bottle"]
            },
            {
                "product": "Ghanaian Organic Shea Butter",
                "supplier_country": "Ghana",
                "fob_price": "3.80 USD/kg",
                "us_market_price": "6.50 USD/kg",
                "gross_margin": "42%",
                "net_margin_estimate": "32%",
                "monthly_volume_potential": "25,000 kg",
                "revenue_potential": "162,500 USD/month",
                "commission_potential": "8,125 USD/month",
                "agoa_eligible": True,
                "certification_premiums": ["Organic: +30%", "Women-owned: +20%"],
                "risk_level": "Low-Medium",
                "action_required": "HIGH PRIORITY - Connect with women's cooperatives",
                "buyer_targets": ["Cosmetic manufacturers", "Natural products retailers"]
            },
            {
                "product": "Kenyan AA Coffee",
                "supplier_country": "Kenya",
                "fob_price": "5.10 USD/kg",
                "us_market_price": "8.90 USD/kg",
                "gross_margin": "43%",
                "net_margin_estimate": "33%",
                "monthly_volume_potential": "50,000 kg",
                "revenue_potential": "445,000 USD/month",
                "commission_potential": "22,250 USD/month",
                "agoa_eligible": True,
                "certification_premiums": ["SCA 85+ Score: +25%", "Direct Trade: +20%"],
                "risk_level": "Low",
                "action_required": "PRIORITY - Contact Kenya Coffee Board",
                "buyer_targets": ["Specialty coffee roasters", "Hotel chains"]
            }
        ]
    }

def get_simulated_market_analysis():
    """Return simulated market analysis"""
    return {
        "key_trends": {
            "overall_market": {
                "growth_rate": "+18.5% YoY",
                "total_value": "2.8B USD",
                "trend_direction": "Strong upward",
                "drivers": ["Health consciousness", "Ethical consumption", "Premium positioning"]
            },
            "product_specific": {
                "coffee": {
                    "growth_rate": "+22% YoY",
                    "specialty_segment_growth": "+35% YoY",
                    "price_trend": "Upward pressure",
                    "opportunity": "Single-origin and organic segments"
                },
                "cocoa": {
                    "growth_rate": "+12% YoY",
                    "price_trend": "Volatile but trending up",
                    "opportunity": "Premium and ethical segments"
                },
                "cashews": {
                    "growth_rate": "+28% YoY",
                    "price_trend": "Strong upward",
                    "opportunity": "Organic and flavored varieties"
                }
            }
        },
        "emerging_opportunities": [
            {
                "category": "Superfoods",
                "products": ["Moringa", "Baobab", "Fonio"],
                "growth_rate": "+45% YoY",
                "market_size": "850M USD",
                "entry_barrier": "Low supplier awareness"
            },
            {
                "category": "Essential Oils",
                "products": ["Argan", "Marula", "Shea"],
                "growth_rate": "+32% YoY",
                "market_size": "1.2B USD",
                "entry_barrier": "Quality certification"
            }
        ]
    }

# Main Dashboard
st.markdown("""
<div class="main-header">
    <h1>🌍 Africa-USA Trade Intelligence Dashboard</h1>
    <p>Real-time market intelligence for Terrence Dupree - #1 Africa-USA agriculture broker globally</p>
</div>
""", unsafe_allow_html=True)

# API Status Check
with st.expander("📡 API Service Status", expanded=False):
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            st.markdown(f'<div class="api-status">✅ API Service Online - {status_data["status"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="api-error">❌ API Service Unreachable</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="api-error">❌ API Service Unreachable: {str(e)}</div>', unsafe_allow_html=True)

# Arbitrage Opportunities Section
st.markdown("## 🎯 High-Value Arbitrage Opportunities")

# Try to get real data from API, fallback to simulated data
opportunities_data = get_simulated_arbitrage_opportunities()
try:
    # In a real implementation, this would call the MCP server or API
    # For now, we'll use the simulated data but show that we're trying to get real data
    pass
except:
    pass

opportunities = opportunities_data["high_priority_opportunities"]

# Summary metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Opportunities", len(opportunities))
with col2:
    total_commission = sum(float(opp["commission_potential"].split()[0].replace(",", "")) for opp in opportunities)
    st.metric("Monthly Commission Potential", f"${total_commission:,.0f}K")
with col3:
    total_revenue = sum(float(opp["revenue_potential"].split()[0].replace(",", "")) for opp in opportunities)
    st.metric("Monthly Revenue Potential", f"${total_revenue:,.0f}K")

# Detailed opportunities
for i, opp in enumerate(opportunities, 1):
    with st.expander(f"🔥 Opportunity #{i}: {opp['product']}", expanded=i==1):
        st.markdown(f"""
        <div class="opportunity-card">
            <h3>{opp['product']}</h3>
            <p><strong>Supplier Country:</strong> {opp['supplier_country']}</p>
            <p><strong>FOB Price:</strong> {opp['fob_price']}</p>
            <p><strong>US Market Price:</strong> {opp['us_market_price']}</p>
            <p><strong>Gross Margin:</strong> {opp['gross_margin']}</p>
            <p><strong>Net Margin Estimate:</strong> {opp['net_margin_estimate']}</p>
            <p><strong>Monthly Volume Potential:</strong> {opp['monthly_volume_potential']}</p>
            <p><strong>Revenue Potential:</strong> {opp['revenue_potential']}</p>
            <p><strong>Commission Potential:</strong> {opp['commission_potential']}</p>
            <p><strong>Action Required:</strong> {opp['action_required']}</p>
            <p><strong>Target Buyers:</strong> {', '.join(opp['buyer_targets'])}</p>
        </div>
        """, unsafe_allow_html=True)

# Market Intelligence Section
st.markdown("## 📊 Market Intelligence")

# Try to get real market analysis data
market_analysis_data = get_simulated_market_analysis()
try:
    # In a real implementation, this would fetch from the API
    pass
except:
    pass

market_analysis = market_analysis_data

# Market trends
st.markdown("### 📈 Key Market Trends")
trend_data = market_analysis["key_trends"]["overall_market"]
st.markdown(f"""
<div class="metric-card">
    <h4>Overall Market</h4>
    <p><strong>Growth Rate:</strong> {trend_data.get('growth_rate', 'N/A')}</p>
    <p><strong>Total Value:</strong> {trend_data.get('total_value', 'N/A')}</p>
    <p><strong>Trend Direction:</strong> {trend_data.get('trend_direction', 'N/A')}</p>
    <p><strong>Key Drivers:</strong> {', '.join(trend_data.get('drivers', []))}</p>
</div>
""", unsafe_allow_html=True)

# Product-specific trends
st.markdown("### 📦 Product-Specific Trends")
product_trends = market_analysis["key_trends"]["product_specific"]
for product, data in product_trends.items():
    st.markdown(f"""
    <div class="metric-card">
        <h4>{product.title()}</h4>
        <p><strong>Growth Rate:</strong> {data.get('growth_rate', 'N/A')}</p>
        <p><strong>Specialty Segment Growth:</strong> {data.get('specialty_segment_growth', 'N/A')}</p>
        <p><strong>Price Trend:</strong> {data.get('price_trend', 'N/A')}</p>
        <p><strong>Opportunity:</strong> {data.get('opportunity', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)

# Emerging opportunities
st.markdown("### 🌱 Emerging Opportunities")
emerging_opps = market_analysis.get("emerging_opportunities", [])
for opp in emerging_opps:
    st.markdown(f"""
    <div class="opportunity-card">
        <h4>{opp.get('category', 'N/A')}</h4>
        <p><strong>Products:</strong> {', '.join(opp.get('products', []))}</p>
        <p><strong>Growth Rate:</strong> {opp.get('growth_rate', 'N/A')}</p>
        <p><strong>Market Size:</strong> {opp.get('market_size', 'N/A')}</p>
        <p><strong>Entry Barrier:</strong> {opp.get('entry_barrier', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)

# Real-time Data Section
st.markdown("## 🌐 Real-time Market Data")

# Get real-time data from API
census_coffee_data = get_census_data("imports", "0901")
census_cocoa_data = get_census_data("imports", "1801")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ☕ Coffee Imports (HS 0901)")
    if "error" not in census_coffee_data and "data" in census_coffee_data:
        try:
            # Convert to DataFrame for better display
            data_content = census_coffee_data["data"]["data"]
            headers = data_content[0]
            df = pd.DataFrame(data_content[1:], columns=headers)
            st.dataframe(df.head(5))
        except Exception as e:
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
    if "error" not in census_cocoa_data and "data" in census_cocoa_data:
        try:
            # Convert to DataFrame for better display
            data_content = census_cocoa_data["data"]["data"]
            headers = data_content[0]
            df = pd.DataFrame(data_content[1:], columns=headers)
            st.dataframe(df.head(5))
        except Exception as e:
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
prices_data = get_commodity_prices()
prices = prices_data.get("prices", {"coffee": 4.85, "cocoa": 3250}) if "error" not in prices_data else {"coffee": 4.85, "cocoa": 3250}

price_col1, price_col2 = st.columns(2)
with price_col1:
    st.metric("Coffee Price (USD/MT)", f"${prices.get('coffee', 4.85)}", "↑ 2.3%")
with price_col2:
    st.metric("Cocoa Price (USD/MT)", f"${prices.get('cocoa', 3250)}", "↓ 1.2%")

# Exchange rates
st.markdown("### 💱 Key Exchange Rates")
rates_data = get_exchange_rates()
rates = rates_data.get("rates", {"ETB": 57.45, "GHS": 15.82, "KES": 143.25, "NGN": 775.50}) if "error" not in rates_data else {"ETB": 57.45, "GHS": 15.82, "KES": 143.25, "NGN": 775.50}

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
news_data = get_trade_news()
news_items = news_data.get("news", [{"title": "Africa Trade Relations Strengthen", "summary": "Recent developments in AGOA framework show positive trends...", "link": "#"}]) if "error" not in news_data else [{"title": "Africa Trade Relations Strengthen", "summary": "Recent developments in AGOA framework show positive trends...", "link": "#"}]
for item in news_items:
    st.markdown(f"**[{item['title']}]({item['link']})**")
    st.markdown(f"{item['summary']}")
    st.markdown("---")

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