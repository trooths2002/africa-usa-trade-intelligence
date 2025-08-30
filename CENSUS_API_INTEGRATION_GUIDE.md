# U.S. Census Bureau API Integration Guide
## For Africa-USA Agriculture Trade Intelligence Platform

This guide explains how to use the U.S. Census Bureau API integration in your FREE WORLD TRADE project to access real-time trade data for Africa-USA agricultural trade.

## 📋 Overview

The U.S. Census Bureau provides free access to comprehensive international trade data through their API. This integration allows you to:

- Track U.S. agricultural exports to African countries
- Monitor U.S. agricultural imports from African countries
- Analyze trade trends and identify opportunities
- Support arbitrage detection and market intelligence

## 🚀 Key API Endpoints

### 1. Monthly U.S. Exports by Harmonized System (HS) Code
```
https://api.census.gov/data/timeseries/intltrade/exports/hs
```
- Track what the U.S. is exporting to African countries
- Useful for identifying market gaps and opportunities

### 2. Monthly U.S. Imports by Harmonized System (HS) Code
```
https://api.census.gov/data/timeseries/intltrade/imports/hs
```
- Monitor what the U.S. is importing from African countries
- Essential for understanding current trade flows

### 3. Monthly U.S. Imports by End-use Code
```
https://api.census.gov/data/timeseries/intltrade/imports/enduse
```
- Understand how imported goods are being used in the U.S. market

## 📊 Important Agricultural HS Codes

| Product | HS Code | Description |
|---------|---------|-------------|
| Coffee | 0901 | Coffee, whether or not roasted |
| Cocoa | 1801 | Cocoa beans, whole or broken |
| Cashews | 0801 | Cashews, shelled or unshelled |
| Spices | 0910 | Mixed spices, unspecified |
| Shea Butter | 1515 | Shea butter and other nuts |
| Vanilla | 0905 | Vanilla beans |
| Tea | 0902 | Tea, whether or not flavored |

## 🌍 African Country Codes

| Country | Code | Key Agricultural Exports |
|---------|------|--------------------------|
| Ethiopia | 5300 | Coffee, oilseeds, pulses |
| Ghana | 7490 | Cocoa, gold, timber |
| Kenya | 5400 | Tea, coffee, flowers |
| Nigeria | 5650 | Oil, cocoa, rubber |
| South Africa | 7020 | Gold, diamonds, fruits |
| Tanzania | 5200 | Gold, coffee, tobacco |
| Uganda | 5350 | Coffee, fish, cotton |
| Côte d'Ivoire | 7320 | Cocoa, coffee, palm oil |
| Rwanda | 5450 | Coffee, tea, tin |
| Morocco | 5000 | Phosphates, citrus fruits |

## 🛠 Implementation Examples

### Python Function to Get Trade Data

```python
import requests

def get_census_trade_data(trade_type="imports", year="2023", month="12", country_code=None, commodity_code=None):
    """Get trade data from U.S. Census Bureau API"""
    try:
        # Select appropriate endpoint
        if trade_type == "exports":
            endpoint = "https://api.census.gov/data/timeseries/intltrade/exports/hs"
            params = {
                "get": "E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR",
                "YEAR": year,
                "MONTH": month
            }
            if commodity_code:
                params["E_COMMODITY"] = commodity_code
        else:
            endpoint = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
            params = {
                "get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC",
                "YEAR": year,
                "MONTH": month
            }
            if country_code:
                params["CTY_CODE"] = country_code
            if commodity_code:
                params["E_COMMODITY"] = commodity_code
        
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Example usage:
# Get coffee imports from Ghana
coffee_data = get_census_trade_data("imports", "2023", "12", country_code="7490", commodity_code="0901")
```

## 📈 Sample API Calls

### 1. U.S. Coffee Exports to Africa
```
GET https://api.census.gov/data/timeseries/intltrade/exports/hs?get=E_COMMODITY,E_COMMODITY_LDESC,ALL_VAL_MO,ALL_VAL_YR&E_COMMODITY=0901&YEAR=2023&MONTH=12
```

### 2. U.S. Cocoa Imports from Ghana
```
GET https://api.census.gov/data/timeseries/intltrade/imports/hs?get=CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC&CTY_CODE=7490&YEAR=2023&MONTH=12
```

### 3. U.S. Cashew Imports from Africa (All Countries)
```
GET https://api.census.gov/data/timeseries/intltrade/imports/hs?get=CTY_CODE,CTY_NAME,GEN_VAL_MO,CON_VAL_MO,E_COMMODITY,E_COMMODITY_LDESC&E_COMMODITY=0801&YEAR=2023
```

## 🔧 Testing the Integration

To test the API integration:

1. Run the test script:
   ```
   python scripts/test_census_api.py
   ```

2. Check the dashboard for real-time data:
   ```
   streamlit run src/web_app/dashboard/main.py
   ```

3. Verify that trade data is being displayed correctly

## ⚠️ Important Notes

1. **No API Key Required**: The Census API works without an API key but has rate limits
2. **Rate Limiting**: Be respectful of API usage - implement delays between requests
3. **Data Availability**: Monthly data is typically available with a 1-2 month lag
4. **Free Service**: This is a completely free government service with no cost

## 📚 Additional Resources

- [U.S. Census Bureau International Trade API Documentation](https://www.census.gov/data/developers/data-sets/international-trade.html)
- [Harmonized System (HS) Code Reference](https://www.census.gov/foreign-trade/schedules/b/2022/hs.pdf)
- [Guide to Using U.S. International Trade Datasets in the Census API](https://www.census.gov/data/developers/data-sets/international-trade.html)

## 🆘 Support

For questions about the U.S. international trade data, contact:
- Phone: 1(800)549-0595 option #4
- Email: eid.international.trade.data@census.gov

This integration provides the foundation for real-time market intelligence to support your goal of becoming the #1 Africa-USA agriculture broker.