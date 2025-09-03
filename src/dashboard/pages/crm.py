#!/usr/bin/env python3
"""
CRM Page for Africa-USA Trade Intelligence Platform
Manage suppliers, buyers, leads, quotes, and shipments
"""
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from src.config.settings import DATABASE_URL

# Page configuration
st.set_page_config(
    page_title="CRM - Africa-USA Trade Intelligence",
    page_icon="👥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .crm-header {
        background: linear-gradient(90deg, #2a5298 0%, #1e3c72 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .crm-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .crm-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
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
<div class="crm-header">
    <h1>👥 Customer Relationship Management</h1>
    <p>Manage suppliers, buyers, leads, quotes, and shipments</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different CRM sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Suppliers", "Buyers", "Leads", "Quotes", "Shipments"])

# Suppliers Tab
with tab1:
    st.header("African Suppliers")
    
    # Add new supplier form
    with st.expander("➕ Add New Supplier"):
        with st.form("new_supplier_form"):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name")
                contact_person = st.text_input("Contact Person")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                country = st.selectbox("Country", ["Ethiopia", "Ghana", "Kenya", "Nigeria", "South Africa", "Other"])
            with col2:
                region = st.text_input("Region/State")
                products = st.text_area("Products (comma-separated)")
                certification = st.text_input("Certifications")
                reliability_score = st.slider("Reliability Score", 0.0, 1.0, 0.8, 0.1)
                payment_terms = st.selectbox("Payment Terms", ["COD", "Net 30", "Net 60", "Other"])
            
            submit_button = st.form_submit_button("Add Supplier")
            
            if submit_button:
                if company_name:
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO suppliers 
                            (company_name, contact_person, email, phone, country, region, products, 
                             certification, reliability_score, payment_terms)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (company_name, contact_person, email, phone, country, region, products,
                              certification, reliability_score, payment_terms))
                        conn.commit()
                        conn.close()
                        st.success("Supplier added successfully!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error adding supplier: {e}")
                else:
                    st.warning("Please enter a company name")
    
    # Display suppliers
    try:
        conn = get_db_connection()
        suppliers_df = pd.read_sql_query("SELECT * FROM suppliers ORDER BY created_at DESC", conn)
        conn.close()
        
        if not suppliers_df.empty:
            st.dataframe(suppliers_df.drop(columns=['created_at', 'updated_at']))
        else:
            st.info("No suppliers found. Add your first supplier using the form above.")
    except Exception as e:
        st.error(f"Error loading suppliers: {e}")

# Buyers Tab
with tab2:
    st.header("US Buyers")
    
    # Add new buyer form
    with st.expander("➕ Add New Buyer"):
        with st.form("new_buyer_form"):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name", key="buyer_company")
                contact_person = st.text_input("Contact Person", key="buyer_contact")
                email = st.text_input("Email", key="buyer_email")
                phone = st.text_input("Phone", key="buyer_phone")
                industry = st.selectbox("Industry", ["Retail", "Manufacturing", "Food Service", "Other"], key="buyer_industry")
            with col2:
                target_products = st.text_area("Target Products (comma-separated)", key="buyer_products")
                annual_volume = st.number_input("Annual Volume (tons)", min_value=0.0, step=10.0, key="buyer_volume")
                credit_rating = st.selectbox("Credit Rating", ["AAA", "AA", "A", "BBB", "BB", "B", "Other"], key="buyer_credit")
                payment_terms = st.selectbox("Payment Terms", ["COD", "Net 30", "Net 60", "Net 90", "Other"], key="buyer_terms")
            
            submit_button = st.form_submit_button("Add Buyer")
            
            if submit_button:
                if company_name:
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO buyers 
                            (company_name, contact_person, email, phone, industry, target_products, 
                             annual_volume, credit_rating, payment_terms)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (company_name, contact_person, email, phone, industry, target_products,
                              annual_volume, credit_rating, payment_terms))
                        conn.commit()
                        conn.close()
                        st.success("Buyer added successfully!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error adding buyer: {e}")
                else:
                    st.warning("Please enter a company name")
    
    # Display buyers
    try:
        conn = get_db_connection()
        buyers_df = pd.read_sql_query("SELECT * FROM buyers ORDER BY created_at DESC", conn)
        conn.close()
        
        if not buyers_df.empty:
            st.dataframe(buyers_df.drop(columns=['created_at', 'updated_at']))
        else:
            st.info("No buyers found. Add your first buyer using the form above.")
    except Exception as e:
        st.error(f"Error loading buyers: {e}")

# Leads Tab
with tab3:
    st.header("Leads & Opportunities")
    
    # Add new lead form
    with st.expander("➕ Add New Lead"):
        with st.form("new_lead_form"):
            col1, col2 = st.columns(2)
            with col1:
                # Get suppliers and buyers for dropdowns
                try:
                    conn = get_db_connection()
                    suppliers = pd.read_sql_query("SELECT id, company_name FROM suppliers", conn)
                    buyers = pd.read_sql_query("SELECT id, company_name FROM buyers", conn)
                    conn.close()
                    
                    supplier_options = dict(zip(suppliers['id'], suppliers['company_name']))
                    buyer_options = dict(zip(buyers['id'], buyers['company_name']))
                    
                    supplier_id = st.selectbox("Supplier", options=list(supplier_options.keys()), 
                                             format_func=lambda x: supplier_options[x])
                    buyer_id = st.selectbox("Buyer", options=list(buyer_options.keys()), 
                                          format_func=lambda x: buyer_options[x])
                    product = st.text_input("Product")
                except Exception as e:
                    st.error(f"Error loading suppliers/buyers: {e}")
                    supplier_id = st.number_input("Supplier ID", min_value=1)
                    buyer_id = st.number_input("Buyer ID", min_value=1)
                    product = st.text_input("Product")
                
                description = st.text_area("Description")
                estimated_value = st.number_input("Estimated Value (USD)", min_value=0.0, step=1000.0)
            
            with col2:
                probability = st.slider("Probability (%)", 0, 100, 50)
                status = st.selectbox("Status", ["New", "Contacted", "Proposal", "Negotiation", "Closed-Won", "Closed-Lost"])
                next_action = st.text_input("Next Action")
                next_action_date = st.date_input("Next Action Date")
                assigned_to = st.text_input("Assigned To", "Terrence Dupree")
            
            submit_button = st.form_submit_button("Add Lead")
            
            if submit_button:
                if product:
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO leads 
                            (supplier_id, buyer_id, product, description, estimated_value, 
                             probability, status, next_action, next_action_date, assigned_to)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (supplier_id, buyer_id, product, description, estimated_value,
                              probability/100, status, next_action, next_action_date, assigned_to))
                        conn.commit()
                        conn.close()
                        st.success("Lead added successfully!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error adding lead: {e}")
                else:
                    st.warning("Please enter a product")
    
    # Display leads
    try:
        conn = get_db_connection()
        leads_query = """
            SELECT l.*, s.company_name as supplier_name, b.company_name as buyer_name
            FROM leads l
            LEFT JOIN suppliers s ON l.supplier_id = s.id
            LEFT JOIN buyers b ON l.buyer_id = b.id
            ORDER BY l.created_at DESC
        """
        leads_df = pd.read_sql_query(leads_query, conn)
        conn.close()
        
        if not leads_df.empty:
            # Format probability as percentage
            leads_df['probability'] = leads_df['probability'].apply(lambda x: f"{x*100:.0f}%")
            st.dataframe(leads_df.drop(columns=['created_at', 'updated_at']))
        else:
            st.info("No leads found. Add your first lead using the form above.")
    except Exception as e:
        st.error(f"Error loading leads: {e}")

# Quotes Tab
with tab4:
    st.header("Quotes")
    st.info("Quote management functionality will be implemented in the next iteration.")

# Shipments Tab
with tab5:
    st.header("Shipments")
    st.info("Shipment tracking functionality will be implemented in the next iteration.")

# Footer
st.markdown("---")
st.markdown("### 🚀 Free World Trade Inc. - Terrence Dupree")
st.markdown("World's #1 Africa-USA Agriculture Broker - Driving Global Trade Excellence")