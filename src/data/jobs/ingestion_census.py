#!/usr/bin/env python3
"""
Census Data Ingestion Job
Fetches and caches US Census data for trade intelligence
"""
import os
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from config.settings import DATABASE_URL
import time
import random

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

def fetch_census_data():
    """
    Fetch US Census trade data
    """
    try:
        # Example API endpoint - replace with actual Census API
        url = "https://api.census.gov/data/timeseries/intltrade/imports/statehs"
        params = {
            "get": "YEAR,MONTH,STATE,PRODUCTCODE,PRODUCTDESCRIPTION,GENERICDESCRIPTION,VALUE",
            "YEAR": "2023",
            "MONTH": "12",
            " PRODUCTCODE": "0701"  # Example: Live cattle
        }
        
        response = fetch_with_retry(url, params)
        if response and response.status_code == 200:
            return response.json()
        elif response:
            print(f"Failed to fetch Census data: {response.status_code}")
            return None
        else:
            print("Failed to fetch Census data after retries")
            return None
    except Exception as e:
        print(f"Error fetching Census data: {e}")
        return None

def save_to_database(data):
    """
    Save fetched data to database
    """
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.DataFrame(data)
        df['timestamp'] = datetime.now()
        df.to_sql('census_data', engine, if_exists='append', index=False)
        print("Census data saved to database")
    except Exception as e:
        print(f"Error saving Census data to database: {e}")

def main():
    """
    Main ingestion job
    """
    print("Starting Census data ingestion job...")
    data = fetch_census_data()
    if data:
        save_to_database(data)
    print("Census data ingestion job completed")

if __name__ == "__main__":
    main()