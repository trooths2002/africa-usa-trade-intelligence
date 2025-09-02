"""
Data collection service for the Africa-USA Trade Intelligence Platform
"""
import requests
import pandas as pd
from typing import Dict, Any, Optional
import time
from datetime import datetime
import json
import sys
import os
import feedparser

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DataCollector:
    def __init__(self):
        self.cache = {}
        self.cache_expiry = {}
        self.use_real = os.getenv("USE_REAL_APIS", "0") == "1"
    
    def get_census_data(self, trade_type: str = "imports", commodity_code: str = None) -> Dict[str, Any]:
        """Get Census trade data. Uses real API when USE_REAL_APIS=1, else returns sample."""
        cache_key = f"census_{trade_type}_{commodity_code}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Default sample data (shape similar to Census output)
        data = {
            "data": [
                ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
                ["7490", "GHANA", "15000000", "14500000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
                ["5300", "ETHIOPIA", "8500000", "8200000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
                ["7320", "COTE D'IVOIRE", "12000000", "11500000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."]
            ],
            "timestamp": time.time()
        }
        
        if self.use_real:
            try:
                # Attempt to query International Trade time series (imports by country)
                # Dataset reference: https://api.census.gov/data/timeseries/intltrade/imports/cty.html
                endpoint = "https://api.census.gov/data/timeseries/intltrade/imports/cty"
                params = {
                    "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,I_COMMODITY,I_COMMODITY_LDESC",
                    # last 12 months
                    "time": "from+2024",
                }
                if commodity_code:
                    # Filter for commodity code if provided
                    params["I_COMMODITY"] = commodity_code
                resp = requests.get(endpoint, params=params, timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    # Expect first row as headers
                    if isinstance(payload, list) and len(payload) > 1:
                        data = {"data": payload, "timestamp": time.time()}
            except Exception:
                # Fall back to sample on any error
                pass
        
        self._cache_data(cache_key, data)
        return data
    
    def get_exchange_rates(self) -> Dict[str, Any]:
        """Get exchange rates (USD base). Uses real API when USE_REAL_APIS=1, else returns sample."""
        cache_key = "exchange_rates"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        data = {
            "rates": {
                "ETB": 57.45,
                "GHS": 15.82,
                "KES": 143.25,
                "NGN": 775.50
            },
            "timestamp": time.time()
        }
        
        if self.use_real:
            try:
                resp = requests.get("https://api.exchangerate.host/latest", params={"base": "USD"}, timeout=10)
                if resp.status_code == 200:
                    payload = resp.json()
                    if isinstance(payload, dict) and "rates" in payload:
                        data = {"rates": payload["rates"], "timestamp": time.time()}
            except Exception:
                pass
        
        self._cache_data(cache_key, data)
        return data
    
    def get_commodity_prices(self) -> Dict[str, Any]:
        """Get commodity prices. Uses real API (World Bank for coffee) when USE_REAL_APIS=1, else sample."""
        cache_key = "commodity_prices"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        data = {
            "prices": {
                "coffee": 4.85,   # USD/lb (sample)
                "cocoa": 3250,    # USD/metric ton (sample)
                "cashews": 8.25   # USD/kg (sample)
            },
            "timestamp": time.time()
        }
        
        if self.use_real:
            try:
                # World Bank indicator for coffee price in USD per kg/ton depends on series. We use PCOFFOTMUSD.
                url = "https://api.worldbank.org/v2/country/WLD/indicator/PCOFFOTMUSD"
                params = {"format": "json", "per_page": "1"}
                resp = requests.get(url, params=params, timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    # payload[1] is list of observations
                    if isinstance(payload, list) and len(payload) > 1 and payload[1]:
                        value = payload[1][0].get("value")
                        if value is not None:
                            # Put under 'coffee' and keep others from sample
                            data["prices"]["coffee"] = value
            except Exception:
                pass
        
        self._cache_data(cache_key, data)
        return data
    
    def get_trade_news(self) -> Dict[str, Any]:
        """Get trade news via RSS when USE_REAL_APIS=1, else sample."""
        cache_key = "trade_news"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        data = {
            "news": [
                {
                    "title": "Africa Trade Relations Strengthen",
                    "summary": "Recent developments in AGOA framework show positive trends...",
                    "link": "#"
                },
                {
                    "title": "Ethiopian Coffee Exports Reach Record High",
                    "summary": "Ethiopian coffee exports to the USA have increased by 25% this quarter...",
                    "link": "#"
                }
            ],
            "timestamp": time.time()
        }
        
        if self.use_real:
            try:
                feeds = [
                    "https://feeds.reuters.com/reuters/businessNews",
                    "http://feeds.bbci.co.uk/news/business/rss.xml",
                ]
                news_items = []
                for f in feeds:
                    parsed = feedparser.parse(f)
                    for entry in parsed.entries[:5]:
                        news_items.append({
                            "title": getattr(entry, "title", ""),
                            "summary": getattr(entry, "summary", ""),
                            "link": getattr(entry, "link", ""),
                        })
                    if news_items:
                        break
                if news_items:
                    data = {"news": news_items, "timestamp": time.time()}
            except Exception:
                pass
        
        self._cache_data(cache_key, data)
        return data
    
    def get_african_exchange_data(self) -> Dict[str, Any]:
        """Get data from African commodity exchanges (sample)."""
        cache_key = "african_exchanges"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Sample data for African exchanges
        data = {
            "exchanges": {
                "NADEX": {
                    "location": "Nigeria",
                    "commodities": ["cocoa", "palm oil", "rubber"],
                    "latest_prices": {
                        "cocoa": 2850,
                        "palm_oil": 950,
                        "rubber": 1650
                    }
                },
                "GSE": {
                    "location": "Ghana",
                    "commodities": ["gold", "cocoa", "timber"],
                    "latest_prices": {
                        "gold": 62000,
                        "cocoa": 2950,
                        "timber": 450
                    }
                },
                "NSE": {
                    "location": "Kenya",
                    "commodities": ["coffee", "tea", "flowers"],
                    "latest_prices": {
                        "coffee": 5200,
                        "tea": 3200,
                        "flowers": 1200
                    }
                }
            },
            "timestamp": time.time()
        }
        
        self._cache_data(cache_key, data)
        return data
    
    def get_social_sentiment(self, keywords: list) -> Dict[str, Any]:
        """Analyze social media sentiment for products (sample)."""
        cache_key = f"social_sentiment_{'_'.join(keywords)}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Sample sentiment data
        data = {
            "keywords": keywords,
            "sentiment_scores": {
                "positive": 0.65,
                "neutral": 0.25,
                "negative": 0.10
            },
            "trending_topics": [
                f"{keywords[0]} quality improvements" if keywords else "quality improvements",
                f"{keywords[1]} market demand" if len(keywords) > 1 else "market demand",
                "sustainable farming practices"
            ],
            "timestamp": time.time()
        }
        
        self._cache_data(cache_key, data)
        return data
    
    def _is_cache_valid(self, key: str, expiry_minutes: int = 30) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        
        if key not in self.cache_expiry:
            return False
        
        return (time.time() - self.cache_expiry[key]) < (expiry_minutes * 60)
    
    def _cache_data(self, key: str, data: Any) -> None:
        """Cache data with timestamp"""
        self.cache[key] = data
        self.cache_expiry[key] = time.time()
