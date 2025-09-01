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

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DataCollector:
    def __init__(self):
        self.cache = {}
        self.cache_expiry = {}
    
    def get_census_data(self, trade_type: str = "imports", commodity_code: str = None) -> Dict[str, Any]:
        """Get Census trade data"""
        cache_key = f"census_{trade_type}_{commodity_code}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # In a real implementation, this would call the actual API
        # For now, we'll return sample data
        data = {
            "data": [
                ["CTY_CODE", "CTY_NAME", "GEN_VAL_MO", "CON_VAL_MO", "I_COMMODITY", "I_COMMODITY_LDESC"],
                ["7490", "GHANA", "15,000,000", "14,500,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
                ["5300", "ETHIOPIA", "8,500,000", "8,200,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."],
                ["7320", "COTE D'IVOIRE", "12,000,000", "11,500,000", "0901", "COFFEE, WHETHER OR NOT ROASTED..."]
            ],
            "timestamp": time.time()
        }
        
        self._cache_data(cache_key, data)
        return data
    
    def get_exchange_rates(self) -> Dict[str, Any]:
        """Get exchange rates"""
        cache_key = "exchange_rates"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Sample data
        data = {
            "rates": {
                "ETB": 57.45,
                "GHS": 15.82,
                "KES": 143.25,
                "NGN": 775.50
            },
            "timestamp": time.time()
        }
        
        self._cache_data(cache_key, data)
        return data
    
    def get_commodity_prices(self) -> Dict[str, Any]:
        """Get commodity prices"""
        cache_key = "commodity_prices"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Sample data
        data = {
            "prices": {
                "coffee": 4.85,
                "cocoa": 3250,
                "cashews": 8.25
            },
            "timestamp": time.time()
        }
        
        self._cache_data(cache_key, data)
        return data
    
    def get_trade_news(self) -> Dict[str, Any]:
        """Get trade news"""
        cache_key = "trade_news"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Sample data
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
        
        self._cache_data(cache_key, data)
        return data
    
    def get_african_exchange_data(self) -> Dict[str, Any]:
        """Get data from African commodity exchanges"""
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
        """Analyze social media sentiment for products"""
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
                f"{keywords[0]} quality improvements",
                f"{keywords[1]} market demand",
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