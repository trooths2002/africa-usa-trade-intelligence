#!/usr/bin/env python3
"""
Test script for dashboard API functions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'web_app', 'dashboard'))

from main import get_census_trade_data
import json

def test_census_api():
    print("Testing Census API functions...")
    
    # Test coffee imports
    print("\n1. Testing coffee imports (HS 0901)...")
    coffee_data = get_census_trade_data("imports", "2023", "12", commodity_code="0901")
    if coffee_data:
        print(f"   SUCCESS: Retrieved {len(coffee_data)} records")
        print(f"   Sample: {coffee_data[:2]}")
    else:
        print("   FAILED: Could not retrieve coffee data")
    
    # Test cocoa imports
    print("\n2. Testing cocoa imports (HS 1801)...")
    cocoa_data = get_census_trade_data("imports", "2023", "12", commodity_code="1801")
    if cocoa_data:
        print(f"   SUCCESS: Retrieved {len(cocoa_data)} records")
        print(f"   Sample: {cocoa_data[:2]}")
    else:
        print("   FAILED: Could not retrieve cocoa data")
    
    # Test exports
    print("\n3. Testing coffee exports...")
    coffee_exports = get_census_trade_data("exports", "2023", "12", commodity_code="0901")
    if coffee_exports:
        print(f"   SUCCESS: Retrieved {len(coffee_exports)} records")
        print(f"   Sample: {coffee_exports[:2]}")
    else:
        print("   FAILED: Could not retrieve coffee exports data")

if __name__ == "__main__":
    test_census_api()