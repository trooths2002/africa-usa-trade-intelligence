#!/usr/bin/env python3
"""
FX Rates Ingestion Job
Fetches and caches foreign exchange rates for African currencies
"""
import os
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import time
import random

# Now we can import settings
try:
    from config.settings import DATABASE_URL
except ImportError:
    # Fallback to environment variable or default
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trade_intelligence.db")

def fetch_with_retry(url, params, max_retries=3):
    """
    Fetch data with exponential backoff retry logic
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response
            elif response.status_code in [429, 500, 502, 503, 504]:
                # Retryable errors
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Attempt {attempt + 1} failed with status {response.status_code}. Retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                    continue
            # Non-retryable error or final attempt
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Attempt {attempt + 1} failed with exception: {e}. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)
                continue
            else:
                raise
    return None

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
            
        response = fetch_with_retry(url, params)
        if response and response.status_code == 200:
            return response.json()
        elif response:
            print(f"Failed to fetch FX rates: {response.status_code}")
            return None
        else:
            print("Failed to fetch FX rates after retries")
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