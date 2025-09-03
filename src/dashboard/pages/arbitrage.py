#!/usr/bin/env python3
"""
Arbitrage Opportunities Page for Africa-USA Trade Intelligence Platform
Display and analyze arbitrage opportunities in agricultural commodities
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from src.config.settings import DATABASE_URL

# Page configuration
st.set_page_config(
    page_title="Arbitrage Opportunities - Africa-USA Trade Intelligence",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .arbitrage-header {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .opportunity-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .high-opportunity {
        border-left: 4px solid #28a745;
        background: #d4edda;
    }
    .medium-opportunity {
        border-left: 4px solid #ffc107;
        background: #fff3cd;
    }
    .low-opportunity {
        border-left: 4px solid #dc3545;
        background: #f8d7da;
    }
</style>
""", unsafe_allow_html=True)

# Database connection helper
def get_db_connection():
    """Get database connection"""
    # Extract the database file path from DATABASE_URL
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        return sqlite3.connect(db_path)
    else:
        # For PostgreSQL, you would use a different connection method
        raise NotImplementedError("Only SQLite is supported in this example")

# Header
st.markdown("""
<div class="arbitrage-header">
    <h1>🎯 Arbitrage Opportunities</h1>
    <p>High-value agricultural commodity arbitrage between Africa and USA</p>
</div>
""", unsafe_allow_html=True)

# Key metrics
try:
    conn = get_db_connection()
    opportunities_df = pd.read_sql_query("SELECT * FROM arbitrage_opportunities ORDER BY timestamp DESC", conn)
    conn.close()
    
    total_opportunities = len(opportunities_df)
    high_margin_opportunities = len(opportunities_df[opportunities_df['gross_margin'] >= 0.40])
    total_commission_potential = opportunities_df['commission_potential_usd'].sum() if not opportunities_df.empty else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Opportunities", total_opportunities)
    col2.metric("High Margin (>40%)", high_margin_opportunities)
    col3.metric("Total Commission Potential", f"${total_commission_potential:,.0f}")
except Exception as e:
    st.error(f"Error loading arbitrage data: {e}")
    opportunities_df = pd.DataFrame()

# Filters
st.markdown("### 🔍 Filter Opportunities")
col1, col2, col3 = st.columns(3)
with col1:
    min_margin = st.slider("Minimum Gross Margin (%)", 0, 100, 20)
with col2:
    country_filter = st.multiselect("Origin Country", 
                                   opportunities_df['origin_country'].unique().tolist() if not opportunities_df.empty else [],
                                   default=opportunities_df['origin_country'].unique().tolist() if not opportunities_df.empty else [])
with col3:
    product_filter = st.multiselect("Product", 
                                   opportunities_df['product'].unique().tolist() if not opportunities_df.empty else [],
                                   default=opportunities_df['product'].unique().tolist() if not opportunities_df.empty else [])

# Apply filters
filtered_df = opportunities_df.copy()
if not filtered_df.empty:
    filtered_df = filtered_df[filtered_df['gross_margin'] >= min_margin/100]
    if country_filter:
        filtered_df = filtered_df[filtered_df['origin_country'].isin(country_filter)]
    if product_filter:
        filtered_df = filtered_df[filtered_df['product'].isin(product_filter)]

# Display opportunities
if not filtered_df.empty:
    st.markdown("### 📊 Arbitrage Opportunities")
    
    # Sort by commission potential
    filtered_df = filtered_df.sort_values('commission_potential_usd', ascending=False)
    
    # Display as cards
    for _, opp in filtered_df.iterrows():
        # Determine card style based on margin
        if opp['gross_margin'] >= 0.40:
            card_class = "high-opportunity"
        elif opp['gross_margin'] >= 0.30:
            card_class = "medium-opportunity"
        else:
            card_class = "low-opportunity"
        
        st.markdown(f"""
        <div class="opportunity-card {card_class}">
            <h3>{opp['product']} 🚀</h3>
            <p><strong>Origin:</strong> {opp['origin_country']} | <strong>Export Price:</strong> ${opp['export_price_usd']} USD/kg | <strong>US Market Price:</strong> ${opp['us_market_price_usd']} USD/kg</p>
            <p><strong>Gross Margin:</strong> <span style="font-size: 1.2em; font-weight: bold;">{opp['gross_margin']*100:.0f}%</span> | <strong>Net Margin:</strong> {opp['net_margin_estimate']*100:.0f}%</p>
            <p><strong>Monthly Volume Potential:</strong> {opp['monthly_volume_potential_tons']:,} tons | <strong>Revenue Potential:</strong> ${opp['revenue_potential_usd']:,.0f} | <strong>Commission Potential:</strong> <span style="color: #28a745; font-weight: bold;">${opp['commission_potential_usd']:,.0f}</span></p>
            <p><strong>AGOA Eligible:</strong> {'✅' if opp['agoa_eligible'] else '❌'} | <strong>Certification Premiums:</strong> {opp['certification_premiums']}</p>
            <p><strong>Risk Level:</strong> {opp['risk_level']} | <strong>Action Required:</strong> <span style="font-weight: bold;">{opp['action_required']}</span></p>
            <p><strong>Buyer Targets:</strong> {opp['buyer_targets']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No arbitrage opportunities found with the current filters.")

# Charts
if not opportunities_df.empty:
    st.markdown("### 📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Margin distribution
        fig1 = px.histogram(opportunities_df, x='gross_margin', nbins=20, 
                           title='Distribution of Gross Margins',
                           labels={'gross_margin': 'Gross Margin', 'count': 'Number of Opportunities'})
        fig1.update_xaxes(tickformat='.0%')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Commission potential by product
        fig2 = px.bar(opportunities_df.groupby('product')['commission_potential_usd'].sum().reset_index(),
                     x='product', y='commission_potential_usd',
                     title='Total Commission Potential by Product',
                     labels={'commission_potential_usd': 'Commission Potential (USD)', 'product': 'Product'})
        fig2.update_yaxes(tickprefix='$')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Commission potential by country
    fig3 = px.bar(opportunities_df.groupby('origin_country')['commission_potential_usd'].sum().reset_index(),
                 x='origin_country', y='commission_potential_usd',
                 title='Total Commission Potential by Origin Country',
                 labels={'commission_potential_usd': 'Commission Potential (USD)', 'origin_country': 'Origin Country'})
    fig3.update_yaxes(tickprefix='$')
    st.plotly_chart(fig3, use_container_width=True)

# Add new opportunity form
with st.expander("➕ Add New Arbitrage Opportunity"):
    with st.form("new_opportunity_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            product = st.text_input("Product")
            origin_country = st.selectbox("Origin Country", ["Ethiopia", "Ghana", "Kenya", "Nigeria", "South Africa", "Other"])
            export_price = st.number_input("Export Price (USD/kg)", min_value=0.0, step=0.1)
            us_market_price = st.number_input("US Market Price (USD/kg)", min_value=0.0, step=0.1)
        with col2:
            monthly_volume = st.number_input("Monthly Volume Potential (tons)", min_value=0.0, step=10.0)
            agoa_eligible = st.checkbox("AGOA Eligible")
            risk_level = st.selectbox("Risk Level", ["Low", "Low-Medium", "Medium", "Medium-High", "High"])
        with col3:
            action_required = st.text_input("Action Required")
            buyer_targets = st.text_area("Buyer Targets (comma-separated)")
            certification_premiums = st.text_input("Certification Premiums")
        
        submit_button = st.form_submit_button("Add Opportunity")
        
        if submit_button:
            if product and export_price and us_market_price:
                # Calculate margins
                if us_market_price > 0:
                    gross_margin = (us_market_price - export_price) / us_market_price
                else:
                    gross_margin = 0
                
                # Estimate values (simplified)
                revenue_potential = us_market_price * monthly_volume * 1000  # Convert tons to kg
                commission_potential = revenue_potential * 0.05  # 5% commission estimate
                net_margin = max(0, gross_margin - 0.10)  # Simplified net margin estimate
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO arbitrage_opportunities 
                        (product, origin_country, export_price_usd, us_market_price_usd, gross_margin,
                         net_margin_estimate, monthly_volume_potential_tons, revenue_potential_usd,
                         commission_potential_usd, agoa_eligible, certification_premiums, risk_level,
                         action_required, buyer_targets)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (product, origin_country, export_price, us_market_price, gross_margin,
                          net_margin, monthly_volume, revenue_potential, commission_potential,
                          agoa_eligible, certification_premiums, risk_level, action_required, buyer_targets))
                    conn.commit()
                    conn.close()
                    st.success("Arbitrage opportunity added successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error adding opportunity: {e}")
            else:
                st.warning("Please fill in all required fields (Product, Export Price, US Market Price)")

# Footer
st.markdown("---")
st.markdown("### 🚀 Free World Trade Inc. - Terrence Dupree")
st.markdown("World's #1 Africa-USA Agriculture Broker - Driving Global Trade Excellence")