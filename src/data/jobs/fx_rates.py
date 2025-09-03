#!/usr/bin/env python3
"""
FX Rates Ingestion Job
Fetches and caches foreign exchange rates for African currencies
"""
import os
import sys
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Now we can import settings
try:
    from src.config.settings import DATABASE_URL
except ImportError:
    # Fallback to environment variable or default
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trade_intelligence.db")

def fetch_fx_rates(base_currency="USD", symbols=None):
    """
    Fetch foreign exchange rates
    Using exchangerate.host API (free tier)
    """
    try:
        url = "https://api.exchangerate.host/latest"
        params = {
            "base": base_currency
        }
        
        if symbols:
            params["symbols"] = ",".join(symbols)
            
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch FX rates: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching FX rates: {e}")
        return None

def process_fx_data(data):
    """
    Process FX data into a structured format
    """
    if not data or "rates" not in data:
        return None
    
    processed_data = []
    timestamp = data.get("timestamp", datetime.now().timestamp())
    date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    base = data.get("base", "USD")
    
    for currency, rate in data["rates"].items():
        processed_data.append({
            'base_currency': base,
            'target_currency': currency,
            'rate': float(rate),
            'date': date,
            'timestamp': datetime.fromtimestamp(timestamp) if timestamp else datetime.now()
        })
    
    return processed_data

def save_to_database(data):
    """
    Save fetched data to database
    """
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.DataFrame(data)
        df.to_sql('fx_rates', engine, if_exists='append', index=False)
        print("FX rates saved to database")
    except Exception as e:
        print(f"Error saving FX rates to database: {e}")

def main():
    """
    Main ingestion job
    """
    print("Starting FX rates ingestion job...")
    
    # African currencies relevant to trade
    african_currencies = [
        "ZAR",  # South African Rand
        "NGN",  # Nigerian Naira
        "KES",  # Kenyan Shilling
        "GHS",  # Ghanaian Cedi
        "ETB",  # Ethiopian Birr
        "UGX",  # Ugandan Shilling
        "TZS",  # Tanzanian Shilling
        "MWK",  # Malawian Kwacha
        "ZMW",  # Zambian Kwacha
        "AOA",  # Angolan Kwanza
        "MAD",  # Moroccan Dirham
        "EGP"   # Egyptian Pound
    ]
    
    data = fetch_fx_rates("USD", african_currencies)
    if data:
        processed_data = process_fx_data(data)
        if processed_data:
            save_to_database(processed_data)
    
    print("FX rates ingestion job completed")

if __name__ == "__main__":
    main()