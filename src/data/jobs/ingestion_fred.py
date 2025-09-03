#!/usr/bin/env python3
"""
FRED Data Ingestion Job
Fetches and caches Federal Reserve Economic Data for trade intelligence
"""
import sys
import os

# Add the project root to the Python path
project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
project_root = os.path.abspath(project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from src.config.settings import DATABASE_URL

# Note: FRED requires an API key, but we'll use a placeholder for now
# In production, you would need to get a free API key from https://fred.stlouisfed.org/docs/api/fred/
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY_HERE")

def fetch_fred_series(series_id, observation_start=None, observation_end=None):
    """
    Fetch a FRED data series
    """
    try:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "limit": 1000
        }
        
        if observation_start:
            params["observation_start"] = observation_start
        if observation_end:
            params["observation_end"] = observation_end
            
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch FRED data for {series_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching FRED data for {series_id}: {e}")
        return None

def process_fred_data(data, series_id, series_name):
    """
    Process FRED data into a structured format
    """
    if not data or "observations" not in data:
        return None
    
    processed_data = []
    for observation in data["observations"]:
        if "date" in observation and "value" in observation and observation["value"] != ".":
            try:
                processed_data.append({
                    'series_id': series_id,
                    'series_name': series_name,
                    'date': observation['date'],
                    'value': float(observation['value']),
                    'timestamp': datetime.now()
                })
            except ValueError:
                # Skip non-numeric values
                continue
    
    return processed_data

def save_to_database(data):
    """
    Save fetched data to database
    """
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.DataFrame(data)
        df.to_sql('fred_data', engine, if_exists='append', index=False)
        print("FRED data saved to database")
    except Exception as e:
        print(f"Error saving FRED data to database: {e}")

def main():
    """
    Main ingestion job
    """
    print("Starting FRED data ingestion job...")
    
    # Example economic indicators relevant to agricultural trade
    series_list = [
        ("DEXUSEU", "US-Euro Foreign Exchange Rate"),
        ("T5YIE", "5-Year Breakeven Inflation Rate"),
        ("DGS10", "10-Year Treasury Constant Maturity Rate"),
        ("DTWEXBGS", "Trade Weighted U.S. Dollar Index: Broad, Goods and Services")
    ]
    
    for series_id, series_name in series_list:
        print(f"Fetching {series_name} ({series_id})...")
        data = fetch_fred_series(series_id)
        if data:
            processed_data = process_fred_data(data, series_id, series_name)
            if processed_data:
                save_to_database(processed_data)
    
    print("FRED data ingestion job completed")

if __name__ == "__main__":
    main()