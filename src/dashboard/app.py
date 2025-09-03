#!/usr/bin/env python3
"""
Streamlit Dashboard for Africa-USA Trade Intelligence Platform
Real-time market intelligence for Terrence Dupree - #1 Africa-USA agriculture broker globally
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import os
from dotenv import load_dotenv
import json
# Import database helpers for persistent user state
try:
    from src.dashboard.db import init_db, save_user_state, load_user_state
except ImportError:
    from db import init_db, save_user_state, load_user_state


# Load environment variables
load_dotenv()
# Initialize database for persistent user state
init_db()

# Password-protect dashboard if APP_LOGIN_PASSWORD is set
APP_PASSWORD = os.getenv("APP_LOGIN_PASSWORD")
if APP_PASSWORD:
    if "is_authed" not in st.session_state:
        st.session_state.is_authed = False
    if not st.session_state.is_authed:
        pw = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if pw == APP_PASSWORD:
                st.session_state.is_authed = True
            else:
                st.error("Incorrect password")
        st.stop()

# Load saved user state (filters etc.)
USER_ID = os.getenv("DEFAULT_USER_ID", "default_user")
if "loaded_user_state" not in st.session_state:
    saved_state = load_user_state(USER_ID)
    if saved_state:
        st.session_state.update(saved_state)
    st.session_state.loaded_user_state = True


# Page configuration
st.set_page_config(
    page_title="Africa-USA Trade Intelligence Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
        height: 100%;
    }
    .opportunity-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .error-card {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
        color: #721c24;
    }
    .success-card {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        color: #155724;
    }
    .warning-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration - Use environment variable or default to Render deployment
API_BASE_URL = os.getenv("STREAMLIT_API_URL", "https://africa-usa-trade-intelligence.onrender.com")

# Utility functions
def test_api_connection():
    """Test if the API is reachable"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

def fetch_data(endpoint, params=None):
    """Fetch data from API with error handling"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🌍 Africa-USA Trade Intelligence Dashboard</h1>
    <p>Real-time market intelligence for Terrence Dupree - #1 Africa-USA agriculture broker globally</p>
</div>
""", unsafe_allow_html=True)

# API Status
with st.expander("📡 API Service Status", expanded=True):
    is_connected, status_data = test_api_connection()
    if is_connected:
        st.success(f"✅ API Service Online - Status: {status_data['status'] if status_data else 'Unknown'}")
        st.info(f"API Endpoint: {API_BASE_URL}")
    else:
        st.error("❌ API Service Unreachable")
        st.info(f"Attempting to connect to: {API_BASE_URL}")
        if status_data:
            st.error(f"Error details: {status_data}")

# Custom Report Generator
st.markdown("## 📊 Custom Market Intelligence Report")
with st.form("custom_report_form"):
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name", "Global Foods Inc.")
    with col2:
        product_focus = st.selectbox("Product Focus", ["coffee", "cocoa", "cashews", "palm oil", "rubber", "shea butter", "vanilla"])
    
    submit_button = st.form_submit_button("Generate Report")
    
    if submit_button:
        with st.spinner("Generating custom report..."):
            report_data = fetch_data("custom-report", {"client_name": client_name, "product_focus": product_focus})
            if "error" not in report_data:
                st.success("Report generated successfully!")
                
                # Display report sections
                st.markdown("### Executive Summary")
                st.write(report_data.get("executive_summary", "No summary available"))
                
                st.markdown("### Market Overview")
                overview = report_data.get("market_overview", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Product Focus", overview.get('product_focus', 'N/A'))
                with col2:
                    st.metric("Key Markets", len(overview.get('key_markets', [])))
                with col3:
                    st.metric("Market Size", overview.get('estimated_market_size', 'N/A'))
                
                st.markdown("### Price Analysis")
                price_analysis = report_data.get("price_analysis", {})
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**US Prices**:")
                    us_prices = price_analysis.get("us_prices", {})
                    if us_prices:
                        for key, value in us_prices.items():
                            st.write(f"- {key}: {value}")
                    else:
                        st.write("No US price data available")
                with col2:
                    st.markdown("**African Prices**:")
                    african_prices = price_analysis.get("african_prices", {})
                    if african_prices:
                        for key, value in african_prices.items():
                            st.write(f"- {key}: {value}")
                    else:
                        st.write("No African price data available")
                
                st.markdown("### Recommendations")
                recommendations = report_data.get("recommendations", [])
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"{i}. {rec}")
                else:
                    st.write("No recommendations available")
            else:
                st.error(f"Error generating report: {report_data['error']}")

# African Market Intelligence
st.markdown("## 🌍 African Market Intelligence")
african_data = fetch_data("african-markets")
if "error" not in african_data:
    # Display market sentiment
    sentiment = african_data.get("analysis", {}).get("market_sentiment", "neutral")
    sentiment_color = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}.get(sentiment.lower(), "🟡")
    st.metric("Market Sentiment", f"{sentiment_color} {sentiment.title()}")
    
    # Display top commodities
    st.markdown("### Top Commodities")
    commodities = african_data.get("analysis", {}).get("top_commodities", [])
    if commodities:
        cols = st.columns(min(len(commodities), 5))
        for i, commodity in enumerate(commodities[:5]):
            with cols[i]:
                st.metric(commodity.title(), "Active Market")
    else:
        st.info("No commodity data available")
    
    # Display opportunities
    st.markdown("### Market Opportunities")
    opportunities = african_data.get("opportunities", [])
    if opportunities:
        for opp in opportunities:
            st.markdown(f"""
            <div class="opportunity-card">
                <h4>{opp.get('opportunity_type', 'Opportunity')}</h4>
                <p><strong>Exchange:</strong> {opp.get('exchange', 'N/A')}</p>
                <p><strong>Commodity:</strong> {opp.get('commodity', 'N/A')}</p>
                <p><strong>Action:</strong> {opp.get('action', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No market opportunities available")
else:
    st.error(f"Unable to fetch African market data: {african_data['error']}")

# High-Value Arbitrage Opportunities
st.markdown("## 🎯 High-Value Arbitrage Opportunities")

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
                "certification_premiums": ["Rainforest Alliance: +20%", "UTZ: +15%"],
                "risk_level": "Low",
                "action_required": "Contact Nairobi Coffee Exchange",
                "buyer_targets": ["Premium coffee retailers", "Starbucks", "Peet's Coffee"]
            }
        ]
    }

# Display opportunities
opportunities = get_simulated_arbitrage_opportunities()["high_priority_opportunities"]
cols = st.columns(min(len(opportunities), 3))
for i, opp in enumerate(opportunities):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="opportunity-card">
            <h4>{opp['product']}</h4>
            <p><strong>Supplier Country:</strong> {opp['supplier_country']}</p>
            <p><strong>FOB Price:</strong> {opp['fob_price']}</p>
            <p><strong>US Market Price:</strong> {opp['us_market_price']}</p>
            <p><strong>Gross Margin:</strong> {opp['gross_margin']}</p>
            <p><strong>Commission Potential:</strong> {opp['commission_potential']}</p>
            <p><strong>Risk Level:</strong> {opp['risk_level']}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("### 🚀 Free World Trade Inc. - Terrence Dupree")
st.markdown("World's #1 Africa-USA Agriculture Broker - Driving Global Trade Excellence")
