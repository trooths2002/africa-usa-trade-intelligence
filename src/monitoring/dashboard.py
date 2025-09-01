#!/usr/bin/env python3
"""
Monitoring Dashboard for Africa-USA Trade Intelligence Platform
Web interface to view monitoring results and system status
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="System Monitoring Dashboard",
    page_icon="📊",
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
    .status-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .healthy {
        background: #d4edda;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    .unhealthy {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    .warning {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>📊 System Monitoring Dashboard</h1>
    <p>Real-time monitoring of the Africa-USA Trade Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Load monitoring data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_monitoring_data():
    """Load monitoring data from files"""
    data = {
        "agent_results": [],
        "dashboard_results": []
    }
    
    # Try to load agent monitoring results
    try:
        if os.path.exists("monitoring_results.json"):
            with open("monitoring_results.json", "r") as f:
                data["agent_results"] = json.load(f)
    except Exception as e:
        st.warning(f"Could not load agent monitoring data: {e}")
    
    # Try to load dashboard monitoring results
    try:
        if os.path.exists("dashboard_monitor_results.json"):
            with open("dashboard_monitor_results.json", "r") as f:
                data["dashboard_results"] = json.load(f)
    except Exception as e:
        st.warning(f"Could not load dashboard monitoring data: {e}")
    
    return data

# Get current monitoring data
monitoring_data = load_monitoring_data()

# Display overall system status
st.markdown("## 🚦 Overall System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>API Status</h3>
    """, unsafe_allow_html=True)
    
    if monitoring_data["agent_results"]:
        latest_result = monitoring_data["agent_results"][-1] if monitoring_data["agent_results"] else {}
        api_healthy = latest_result.get("components", {}).get("api", {}).get("healthy", False)
        status_class = "healthy" if api_healthy else "unhealthy"
        status_text = "Healthy" if api_healthy else "Issues Detected"
        st.markdown(f'<div class="status-card {status_class}">{status_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-card warning">No Data</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Dashboard Status</h3>
    """, unsafe_allow_html=True)
    
    if monitoring_data["agent_results"]:
        latest_result = monitoring_data["agent_results"][-1] if monitoring_data["agent_results"] else {}
        dashboard_healthy = latest_result.get("components", {}).get("dashboard", {}).get("healthy", False)
        status_class = "healthy" if dashboard_healthy else "unhealthy"
        status_text = "Healthy" if dashboard_healthy else "Issues Detected"
        st.markdown(f'<div class="status-card {status_class}">{status_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-card warning">No Data</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>System Health</h3>
    """, unsafe_allow_html=True)
    
    if monitoring_data["agent_results"]:
        latest_result = monitoring_data["agent_results"][-1] if monitoring_data["agent_results"] else {}
        overall_healthy = latest_result.get("overall_healthy", False)
        status_class = "healthy" if overall_healthy else "unhealthy"
        status_text = "Healthy" if overall_healthy else "Issues Detected"
        st.markdown(f'<div class="status-card {status_class}">{status_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-card warning">No Data</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Display recent monitoring results
st.markdown("## 📋 Recent Monitoring Results")

if monitoring_data["agent_results"]:
    # Convert to DataFrame for better display
    results_df = pd.DataFrame(monitoring_data["agent_results"][-10:])  # Last 10 results
    
    # Display as table
    st.dataframe(results_df[["timestamp", "overall_healthy"]].tail(10))
    
    # Create health trend chart
    if len(results_df) > 1:
        st.markdown("### Health Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=results_df["timestamp"],
            y=results_df["overall_healthy"].astype(int),
            mode='lines+markers',
            name='System Health',
            line=dict(color='blue')
        ))
        fig.update_layout(
            title="System Health Over Time",
            xaxis_title="Time",
            yaxis_title="Health Status (1=Healthy, 0=Unhealthy)",
            yaxis=dict(tickvals=[0, 1], ticktext=["Unhealthy", "Healthy"])
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No monitoring data available yet. Monitoring agent will start collecting data soon.")

# Display dashboard monitoring results
st.markdown("## 🖥️ Dashboard Monitoring Details")

if monitoring_data["dashboard_results"]:
    dashboard_result = monitoring_data["dashboard_results"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Accessibility")
        accessibility = dashboard_result.get("checks", {}).get("accessibility", {})
        if accessibility.get("passed"):
            st.success("✅ Dashboard is accessible")
            details = accessibility.get("details", {})
            st.write(f"Response Time: {details.get('response_time', 'N/A'):.2f}s")
            st.write(f"Content Length: {details.get('content_length', 'N/A')} bytes")
        else:
            st.error("❌ Dashboard accessibility issues")
            st.write(accessibility.get("details", {}))
    
    with col2:
        st.markdown("### API Connectivity")
        api_connectivity = dashboard_result.get("checks", {}).get("api_connectivity", {})
        if api_connectivity.get("passed"):
            st.success("✅ API connectivity working")
            details = api_connectivity.get("details", {})
            st.write(f"API Status: {details.get('api_status', 'N/A')}")
        else:
            st.error("❌ API connectivity issues")
            st.write(api_connectivity.get("details", {}))
    
    st.markdown("### Interactivity")
    interactivity = dashboard_result.get("checks", {}).get("interactivity", {})
    if interactivity.get("passed"):
        st.success("✅ Dashboard is interactive")
        details = interactivity.get("details", {})
        st.write("All interactive elements found correctly")
    else:
        st.warning("⚠️ Dashboard interactivity check issues")
        st.write(interactivity.get("details", {}))
else:
    st.info("No dashboard monitoring data available yet. Dashboard monitoring will start collecting data soon.")

# Display data endpoint status
st.markdown("## 📡 Data Endpoint Status")

if monitoring_data["agent_results"] and monitoring_data["agent_results"][-1].get("data_endpoints"):
    endpoints = monitoring_data["agent_results"][-1]["data_endpoints"]
    
    for endpoint, result in endpoints.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{endpoint}**")
        with col2:
            status = result.get('status', 'unknown')
            if status == 'success':
                st.success("✅ Success")
            elif status == 'failed':
                st.error("❌ Failed")
            else:
                st.warning("⚠️ Unknown")
        with col3:
            if 'response_time' in result:
                st.write(f"{result['response_time']:.2f}s")
else:
    st.info("No data endpoint status available yet.")

# Footer
st.markdown("---")
st.markdown("### 🤖 Automated Monitoring System")
st.markdown("This dashboard shows the real-time status of the Africa-USA Trade Intelligence Platform.")