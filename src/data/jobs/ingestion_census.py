#!/usr/bin/env python3
"""
Census Data Ingestion Job
Fetches and caches US Census data for trade intelligence
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from src.config.settings import DATABASE_URL

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
            "PRODUCTCODE": "0701"  # Example: Live cattle
        }
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch Census data: {response.status_code}")
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