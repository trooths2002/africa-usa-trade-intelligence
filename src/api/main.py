#!/usr/bin/env python3
"""
API Gateway for Africa-USA Trade Intelligence Platform
Centralized API with caching and monitoring
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
import time
import json
from datetime import datetime, timedelta

# Initialize FastAPI app
app = FastAPI(
    title="Africa-USA Trade Intelligence API Gateway",
    description="Centralized API gateway with caching for trade intelligence",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory cache
class SimpleCache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            entry = self._cache[key]
            # Check if cache is still valid (5 minutes default)
            if datetime.now() < entry["expires"]:
                return entry["data"]
            else:
                # Expire cache
                del self._cache[key]
        return None
    
    def set(self, key: str, data: Any, expiry_minutes: int = 5):
        self._cache[key] = {
            "data": data,
            "expires": datetime.now() + timedelta(minutes=expiry_minutes)
        }

# Initialize cache
cache = SimpleCache()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "API Gateway"
    }

# Census data endpoint
@app.get("/census/{trade_type}/{commodity_code}")
async def get_census_data(trade_type: str, commodity_code: str, year: str = "2023", month: str = "12"):
    """Get trade data from U.S. Census Bureau API"""
    cache_key = f"census_{trade_type}_{commodity_code}_{year}_{month}"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "data": cached_data,
            "cached": True,
            "timestamp": datetime.now().isoformat()
        }
    
    # In a real implementation, this would call the actual Census API
    # For now, we'll return sample data
    sample_data = {
        "trade_type": trade_type,
        "commodity_code": commodity_code,
        "year": year,
        "month": month,
        "data": [
            ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
            ["7490", "GHANA", "15,000,000", "14,500,000", commodity_code, "Sample commodity data"],
            ["5300", "ETHIOPIA", "8,500,000", "8,200,000", commodity_code, "Sample commodity data"]
        ]
    }
    
    # Cache the data for 30 minutes
    cache.set(cache_key, sample_data, expiry_minutes=30)
    
    return {
        "data": sample_data,
        "cached": False,
        "timestamp": datetime.now().isoformat()
    }

# Exchange rates endpoint
@app.get("/exchange-rates")
async def get_exchange_rates():
    """Get exchange rates from free sources"""
    cache_key = "exchange_rates"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "rates": cached_data,
            "cached": True,
            "timestamp": datetime.now().isoformat()
        }
    
    # Sample data
    rates = {
        "ETB": 57.45,  # Ethiopian Birr
        "GHS": 15.82,  # Ghanaian Cedi
        "KES": 143.25, # Kenyan Shilling
        "NGN": 775.50, # Nigerian Naira
        "ZAR": 18.75   # South African Rand
    }
    
    # Cache the data for 60 minutes
    cache.set(cache_key, rates, expiry_minutes=60)
    
    return {
        "rates": rates,
        "cached": False,
        "timestamp": datetime.now().isoformat()
    }

# Commodity prices endpoint
@app.get("/commodity-prices")
async def get_commodity_prices():
    """Get commodity prices from free sources"""
    cache_key = "commodity_prices"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "prices": cached_data,
            "cached": True,
            "timestamp": datetime.now().isoformat()
        }
    
    # Sample data
    prices = {
        "coffee": 4.85,   # USD per kg
        "cocoa": 3250,    # USD per metric ton
        "cashews": 8.20,  # USD per kg
        "shea_butter": 6.50 # USD per kg
    }
    
    # Cache the data for 30 minutes
    cache.set(cache_key, prices, expiry_minutes=30)
    
    return {
        "prices": prices,
        "cached": False,
        "timestamp": datetime.now().isoformat()
    }

# Trade news endpoint
@app.get("/trade-news")
async def get_trade_news():
    """Get trade news from free RSS feeds"""
    cache_key = "trade_news"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "news": cached_data,
            "cached": True,
            "timestamp": datetime.now().isoformat()
        }
    
    # Sample data
    news = [
        {
            "title": "Africa-USA Trade Relations Strengthen Under AGOA",
            "summary": "Recent developments in the African Growth and Opportunity Act framework show positive trends for bilateral trade.",
            "link": "https://example.com/news/1",
            "published": "2025-09-01"
        },
        {
            "title": "Premium African Agricultural Exports Gain Market Share",
            "summary": "Specialty coffee and cocoa from East Africa are commanding higher prices in US markets.",
            "link": "https://example.com/news/2",
            "published": "2025-08-28"
        }
    ]
    
    # Cache the data for 60 minutes
    cache.set(cache_key, news, expiry_minutes=60)
    
    return {
        "news": news,
        "cached": False,
        "timestamp": datetime.now().isoformat()
    }

# Weather data endpoint
@app.get("/weather/{country_code}")
async def get_weather(country_code: str):
    """Get weather data for African countries"""
    cache_key = f"weather_{country_code}"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return {
            "weather": cached_data,
            "country_code": country_code,
            "cached": True,
            "timestamp": datetime.now().isoformat()
        }
    
    # Sample data
    weather_data = {
        "ET": {"country": "Ethiopia", "temperature": "22°C", "conditions": "Sunny", "rainfall": "Moderate"},
        "KE": {"country": "Kenya", "temperature": "26°C", "conditions": "Partly Cloudy", "rainfall": "Low"},
        "GH": {"country": "Ghana", "temperature": "28°C", "conditions": "Rainy", "rainfall": "High"},
        "NG": {"country": "Nigeria", "temperature": "30°C", "conditions": "Sunny", "rainfall": "Low"},
        "ZA": {"country": "South Africa", "temperature": "18°C", "conditions": "Clear", "rainfall": "Minimal"}
    }
    
    weather = weather_data.get(country_code, {"country": "Unknown", "temperature": "N/A", "conditions": "N/A", "rainfall": "N/A"})
    
    # Cache the data for 15 minutes
    cache.set(cache_key, weather, expiry_minutes=15)
    
    return {
        "weather": weather,
        "country_code": country_code,
        "cached": False,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )