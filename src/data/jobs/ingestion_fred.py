#!/usr/bin/env python3
"""
FRED Data Ingestion Job
Fetches and caches Federal Reserve Economic Data for trade intelligence
"""
import os
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from config.settings import DATABASE_URL
import time
import random

# Note: FRED requires an API key, but we'll use a placeholder for now
# In production, you would need to get a free API key from https://fred.stlouisfed.org/docs/api/fred/
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY_HERE")

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
            
        response = fetch_with_retry(url, params)
        if response and response.status_code == 200:
            return response.json()
        elif response:
            print(f"Failed to fetch FRED data for {series_id}: {response.status_code}")
            return None
        else:
            print(f"Failed to fetch FRED data for {series_id} after retries")
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