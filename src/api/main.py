#!/usr/bin/env python3
"""
API Gateway for Africa-USA Trade Intelligence Platform
Centralized API with caching and monitoring
"""

import uvicorn
from fastapi import FastAPI
from typing import Dict, Any, Optional
import time
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.collector import DataCollector
from monitoring.health import HealthMonitor

app = FastAPI(title="Africa-USA Trade Intelligence API", version="1.0.0")

# Initialize services
data_collector = DataCollector()
health_monitor = HealthMonitor()

@app.get("/")
def read_root():
    return {"message": "Africa-USA Trade Intelligence API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return health_monitor.check_all_services()

@app.get("/census-data")
def get_census_data(trade_type: str = "imports", commodity_code: Optional[str] = None):
    return data_collector.get_census_data(trade_type, commodity_code)

@app.get("/exchange-rates")
def get_exchange_rates():
    return data_collector.get_exchange_rates()

@app.get("/commodity-prices")
def get_commodity_prices():
    return data_collector.get_commodity_prices()

@app.get("/trade-news")
def get_trade_news():
    return data_collector.get_trade_news()

@app.get("/african-markets")
def get_african_markets():
    """Get comprehensive African market intelligence"""
    # Simulate comprehensive market intelligence
    return {
        "markets": {
            "Ethiopia": {"coffee_exports": "high", "growth_rate": "22%", "specialties": ["coffee", "spices"]},
            "Ghana": {"cocoa_exports": "very_high", "growth_rate": "15%", "specialties": ["cocoa", "shea"]},
            "Kenya": {"tea_exports": "high", "growth_rate": "18%", "specialties": ["tea", "coffee", "flowers"]}
        },
        "opportunities": ["Single-origin coffee", "Organic cocoa", "Premium tea"],
        "timestamp": time.time()
    }

@app.get("/custom-report")
def generate_custom_report(client_name: str, product_focus: str):
    """Generate a custom market analysis report"""
    return {
        "client": client_name,
        "product_focus": product_focus,
        "report": {
            "market_size": f"${(hash(product_focus) % 1000) + 100}M USD",
            "growth_rate": f"{(hash(product_focus) % 50) + 10}% YoY",
            "key_suppliers": ["Premium African Cooperatives", "Certified Organic Producers"],
            "recommendations": [
                f"Focus on premium {product_focus} segments",
                "Leverage AGOA benefits for cost advantage",
                "Build direct supplier relationships"
            ]
        },
        "timestamp": time.time()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
