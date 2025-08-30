#!/usr/bin/env python3
"""
Simple test script for Census API functions
"""

import requests
import json

def get_census_trade_data(trade_type="imports", year="2023", month="12", country_code=None, commodity_code=None):
    """Get trade data from U.S. Census Bureau API"""
    try:
        # Select appropriate endpoint
        if trade_type == "exports":
            endpoint = "https://api.census.gov/data/timeseries/intltrade/exports/hs"
            params = {
                "get": "E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR,YEAR,MONTH",
                "YEAR": year,
                "MONTH": month
            }
            if commodity_code:
                params["E_COMMODITY"] = commodity_code
        else:
            endpoint = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
            params = {
                "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,I_COMMODITY,I_COMMODITY_LDESC,YEAR,MONTH",
                "YEAR": year,
                "MONTH": month
            }
            if country_code:
                params["CTY_CODE"] = country_code
            if commodity_code:
                params["I_COMMODITY"] = commodity_code
        
        # Add timeout and headers for better reliability
        headers = {
            "User-Agent": "Africa-USA Trade Intelligence Platform (Free World Trade Inc.)"
        }
        
        print(f"Making request to: {endpoint}")
        print(f"Parameters: {params}")
        
        response = requests.get(endpoint, params=params, headers=headers, timeout=30)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully retrieved {len(data)} records")
            return data
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response content: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Error fetching Census trade data: {str(e)}")
        return None

def test_census_api():
    print("Testing Census API functions...")
    
    # Test coffee imports
    print("\n1. Testing coffee imports (HS 0901)...")
    coffee_data = get_census_trade_data("imports", "2023", "12", commodity_code="0901")
    if coffee_data:
        print(f"   SUCCESS: Retrieved {len(coffee_data)} records")
        print(f"   Headers: {coffee_data[0]}")
        print(f"   Sample record: {coffee_data[1] if len(coffee_data) > 1 else 'No data'}")
    else:
        print("   FAILED: Could not retrieve coffee data")
    
    # Test cocoa imports
    print("\n2. Testing cocoa imports (HS 1801)...")
    cocoa_data = get_census_trade_data("imports", "2023", "12", commodity_code="1801")
    if cocoa_data:
        print(f"   SUCCESS: Retrieved {len(cocoa_data)} records")
        print(f"   Headers: {cocoa_data[0]}")
        print(f"   Sample record: {cocoa_data[1] if len(cocoa_data) > 1 else 'No data'}")
    else:
        print("   FAILED: Could not retrieve cocoa data")

if __name__ == "__main__":
    test_census_api()