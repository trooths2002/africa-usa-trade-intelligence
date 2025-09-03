#!/usr/bin/env python3
"""
World Bank Data Ingestion Job
Fetches and caches World Bank commodity price data
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

def fetch_world_bank_data(indicator, country="WLD", start_year="2020", end_year="2025"):
    """
    Fetch World Bank commodity price data
    """
    try:
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}",
            "per_page": "1000"
        }
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch World Bank data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching World Bank data: {e}")
        return None

def process_world_bank_data(data, indicator_name):
    """
    Process World Bank data into a structured format
    """
    if not data or len(data) < 2:
        return None
    
    processed_data = []
    for item in data[1]:  # Second element contains the actual data
        if item and 'date' in item and 'value' in item and item['value'] is not None:
            processed_data.append({
                'indicator': indicator_name,
                'date': item['date'],
                'value': float(item['value']),
                'country': item.get('country', {}).get('value', 'World'),
                'timestamp': datetime.now()
            })
    
    return processed_data

def save_to_database(data):
    """
    Save fetched data to database
    """
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.DataFrame(data)
        df.to_sql('world_bank_data', engine, if_exists='append', index=False)
        print("World Bank data saved to database")
    except Exception as e:
        print(f"Error saving World Bank data to database: {e}")

def main():
    """
    Main ingestion job
    """
    print("Starting World Bank data ingestion job...")
    
    # Coffee prices (US cents per pound)
    coffee_data = fetch_world_bank_data("PCOFFOTMUSD")
    if coffee_data:
        processed_coffee = process_world_bank_data(coffee_data, "Coffee")
        if processed_coffee:
            save_to_database(processed_coffee)
    
    # Cocoa prices (US cents per pound)
    cocoa_data = fetch_world_bank_data("PCOCO_USD")
    if cocoa_data:
        processed_cocoa = process_world_bank_data(cocoa_data, "Cocoa")
        if processed_cocoa:
            save_to_database(processed_cocoa)
    
    # Palm oil prices (US cents per pound)
    palm_oil_data = fetch_world_bank_data("PMPM_USD")
    if palm_oil_data:
        processed_palm_oil = process_world_bank_data(palm_oil_data, "Palm Oil")
        if processed_palm_oil:
            save_to_database(processed_palm_oil)
    
    print("World Bank data ingestion job completed")

if __name__ == "__main__":
    main()