#!/usr/bin/env python3
"""
Test script for U.S. Census Bureau API integration
Validates that the API endpoints are working correctly for Africa-USA trade data
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_census_api_endpoints():
    """Test the Census API endpoints for trade data"""
    print("=" * 80)
    print("🧪 TESTING U.S. CENSUS BUREAU API INTEGRATION")
    print("=" * 80)
    print("🎯 Goal: Validate Africa-USA agriculture trade data collection")
    print("💰 Technology Cost: $0 (100% free resources)")
    print("=" * 80)
    
    # Census API endpoints for international trade
    endpoints = {
        "exports_hs": "https://api.census.gov/data/timeseries/intltrade/exports/hs",
        "imports_hs": "https://api.census.gov/data/timeseries/intltrade/imports/hs",
        "imports_enduse": "https://api.census.gov/data/timeseries/intltrade/imports/enduse"
    }
    
    # Test each endpoint
    for name, url in endpoints.items():
        print(f"\n🔍 Testing {name.upper()} endpoint...")
        print(f"   URL: {url}")
        
        try:
            # Simple test request for recent data
            if "exports" in name:
                # For exports, get coffee data (HS code 0901)
                params = {
                    "get": "E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR",
                    "YEAR": "2023",
                    "MONTH": "12"
                }
            else:
                # For imports, get data for a specific country
                params = {
                    "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO",
                    "YEAR": "2023",
                    "MONTH": "12"
                }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS: Received {len(data)} records")
                print(f"   📊 Sample data: {str(data[:2])[:100]}...")
            else:
                print(f"   ❌ FAILED: Status code {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 80)
    print("📝 EXAMPLE API CALLS FOR AFRICA-USA AGRICULTURE TRADE")
    print("=" * 80)
    
    # Example API calls for specific agricultural products
    examples = [
        {
            "description": "U.S. Coffee Exports to Africa (HS Code 0901)",
            "url": "https://api.census.gov/data/timeseries/intltrade/exports/hs",
            "params": {
                "get": "E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR",
                "E_COMMODITY": "0901",
                "YEAR": "2023",
                "MONTH": "12"
            }
        },
        {
            "description": "U.S. Cocoa Imports from Ghana (CTY_CODE 7490)",
            "url": "https://api.census.gov/data/timeseries/intltrade/imports/hs",
            "params": {
                "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC",
                "CTY_CODE": "7490",
                "YEAR": "2023",
                "MONTH": "12"
            }
        },
        {
            "description": "U.S. Cashew Imports from Africa",
            "url": "https://api.census.gov/data/timeseries/intltrade/imports/hs",
            "params": {
                "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC",
                "E_COMMODITY": "0801",
                "YEAR": "2023"
            }
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   API Call: {example['url']}")
        print(f"   Parameters: {json.dumps(example['params'], indent=10)}")
    
    print("\n" + "=" * 80)
    print("📋 AFRICAN COUNTRY CODES FOR CENSUS API")
    print("=" * 80)
    
    # African country codes for Census API
    african_countries = {
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
    
    for country, code in african_countries.items():
        print(f"   {country}: {code}")

if __name__ == "__main__":
    test_census_api_endpoints()