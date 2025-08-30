#!/usr/bin/env python3
"""
Automated Data Tracker for U.S. Census Bureau API
Regularly fetches and stores trade data for Africa-USA agricultural trade

This script runs periodically to collect trade data and store it locally for analysis
"""

import os
import sys
import json
import csv
import requests
from datetime import datetime, timedelta
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/tracking.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Census API endpoints
CENSUS_ENDPOINTS = {
    "exports_hs": "https://api.census.gov/data/timeseries/intltrade/exports/hs",
    "imports_hs": "https://api.census.gov/data/timeseries/intltrade/imports/hs",
    "imports_enduse": "https://api.census.gov/data/timeseries/intltrade/imports/enduse"
}

# African countries and their codes
AFRICAN_COUNTRIES = {
    "Ethiopia": "5300",
    "Ghana": "7490", 
    "Kenya": "5400",
    "Nigeria": "5650",
    "South Africa": "7020",
    "Tanzania": "5200",
    "Uganda": "5350",
    "Côte d'Ivoire": "7320",
    "Rwanda": "5450",
    "Morocco": "5000"
}

# Key agricultural products and their HS codes
AGRICULTURAL_PRODUCTS = {
    "coffee": "0901",
    "cocoa": "1801",
    "cashews": "0801",
    "spices": "0910",
    "shea_butter": "1515",
    "vanilla": "0905",
    "tea": "0902"
}

def fetch_census_data(endpoint, params):
    """Fetch data from Census API"""
    try:
        logger.info(f"Fetching data from {endpoint} with params {params}")
        response = requests.get(endpoint, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} records")
            return data
        else:
            logger.error(f"API request failed with status {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return None

def save_data_to_csv(data, filename):
    """Save data to CSV file"""
    if not data:
        logger.warning("No data to save")
        return
    
    try:
        filepath = os.path.join("data", "census_data", filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        logger.info(f"Data saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving data to CSV: {str(e)}")

def track_agricultural_exports():
    """Track agricultural exports from the US to Africa"""
    logger.info("Tracking agricultural exports...")
    
    # Track key agricultural products
    for product_name, hs_code in AGRICULTURAL_PRODUCTS.items():
        params = {
            "get": "E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR,YEAR,MONTH",
            "E_COMMODITY": hs_code,
            "YEAR": "2023",
            "MONTH": "12"
        }
        
        data = fetch_census_data(CENSUS_ENDPOINTS["exports_hs"], params)
        if data:
            filename = f"us_exports_{product_name}_2023_12.csv"
            save_data_to_csv(data, filename)
            time.sleep(1)  # Rate limiting

def track_agricultural_imports():
    """Track agricultural imports to the US from Africa"""
    logger.info("Tracking agricultural imports...")
    
    # Track imports from key African countries for key products
    for country, country_code in AFRICAN_COUNTRIES.items():
        for product_name, hs_code in AGRICULTURAL_PRODUCTS.items():
            params = {
                "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC,YEAR,MONTH",
                "CTY_CODE": country_code,
                "E_COMMODITY": hs_code,
                "YEAR": "2023",
                "MONTH": "12"
            }
            
            data = fetch_census_data(CENSUS_ENDPOINTS["imports_hs"], params)
            if data:
                filename = f"us_imports_{product_name}_from_{country}_2023_12.csv"
                save_data_to_csv(data, filename)
                time.sleep(1)  # Rate limiting

def track_monthly_trends():
    """Track monthly trends for the past 6 months"""
    logger.info("Tracking monthly trends...")
    
    # Get data for the last 6 months
    today = datetime.now()
    for i in range(6):
        month_date = today - timedelta(days=30*i)
        year = month_date.year
        month = month_date.month
        
        # Format month as two digits
        month_str = f"{month:02d}"
        
        # Track coffee imports as an example
        params = {
            "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC,YEAR,MONTH",
            "E_COMMODITY": "0901",  # Coffee
            "YEAR": str(year),
            "MONTH": month_str
        }
        
        data = fetch_census_data(CENSUS_ENDPOINTS["imports_hs"], params)
        if data:
            filename = f"monthly_coffee_imports_{year}_{month_str}.csv"
            save_data_to_csv(data, filename)
            time.sleep(1)  # Rate limiting

def create_data_summary():
    """Create a summary of the collected data"""
    logger.info("Creating data summary...")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "african_countries": list(AFRICAN_COUNTRIES.keys()),
        "agricultural_products": list(AGRICULTURAL_PRODUCTS.keys()),
        "data_files_created": []
    }
    
    # List all CSV files in the census_data directory
    try:
        data_dir = os.path.join("data", "census_data")
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            csv_files = [f for f in files if f.endswith('.csv')]
            summary["data_files_created"] = csv_files
    except Exception as e:
        logger.error(f"Error creating summary: {str(e)}")
    
    # Save summary
    try:
        summary_path = os.path.join("data", "census_data", "data_collection_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary saved to {summary_path}")
    except Exception as e:
        logger.error(f"Error saving summary: {str(e)}")

def main():
    """Main function to run the automated data tracker"""
    logger.info("=" * 60)
    logger.info("AUTOMATED CENSUS DATA TRACKER STARTING")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    
    try:
        # Track agricultural exports
        track_agricultural_exports()
        
        # Track agricultural imports
        track_agricultural_imports()
        
        # Track monthly trends
        track_monthly_trends()
        
        # Create summary
        create_data_summary()
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"End time: {end_time}")
        logger.info(f"Total duration: {duration}")
        logger.info("AUTOMATED DATA TRACKING COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error in main tracking process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()