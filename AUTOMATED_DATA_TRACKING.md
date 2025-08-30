# Automated Data Tracking System
## For Africa-USA Agriculture Trade Intelligence Platform

This document explains how the automated data tracking system works in your FREE WORLD TRADE project to collect and store trade data from the U.S. Census Bureau API.

## 📋 System Overview

The automated data tracking system regularly fetches trade data from the U.S. Census Bureau API and stores it locally for analysis. This enables you to:

- Track historical trade trends
- Identify emerging opportunities
- Monitor market changes over time
- Support arbitrage detection with real data

## 🔄 How It Works

### 1. Data Collection Process

The system automatically collects data for:

- **Key Agricultural Products**: Coffee, cocoa, cashews, spices, shea butter, vanilla, tea
- **Key African Trading Partners**: Ethiopia, Ghana, Kenya, Nigeria, South Africa, Tanzania, Uganda, Côte d'Ivoire, Rwanda, Morocco
- **Time Periods**: Monthly data for the current and previous months

### 2. Data Storage

Collected data is stored in:

- **Location**: `data/census_data/` directory
- **Format**: CSV files with descriptive names
- **Organization**: Files are named with product, country, and date information

### 3. Automation

The system can be configured to run automatically:

- **Daily**: Recommended for up-to-date market intelligence
- **Weekly**: For less frequent monitoring
- **Manual**: On-demand collection when needed

## 🛠 System Components

### 1. Initialization Script
**File**: `scripts/init_data_collection.py`
- Sets up data directories
- Creates log files
- Runs initial data collection
- Provides setup instructions for scheduled tasks

### 2. Automated Data Tracker
**File**: `scripts/automated_data_tracker.py`
- Fetches data from Census APIs
- Stores data in CSV format
- Logs collection activities
- Handles errors gracefully

### 3. Scheduled Collection
**File**: `scripts/scheduled_data_collection.py`
- Runs the data tracker on a schedule
- Can be configured with system task schedulers
- Provides logging and monitoring

### 4. MCP Server Integration
**File**: `src/mcp_servers/market_intelligence/server.py`
- Includes data collection functions
- Integrates with the market intelligence system
- Provides real-time data access

## ▶️ Running the System

### Initialize the System
```bash
python scripts/init_data_collection.py
```

### Run Data Collection Manually
```bash
python scripts/automated_data_tracker.py
```

### Set Up Scheduled Collection
Follow the instructions in `data/scheduled_task_setup.txt` to configure automatic daily collection.

## 📁 Data Organization

### Directory Structure
```
data/
├── census_data/
│   ├── us_exports_coffee_2023_12.csv
│   ├── us_imports_cocoa_from_Ghana_2023_12.csv
│   └── data_collection_summary.json
├── suppliers/
├── buyers/
├── market_intelligence/
├── tracking.log
└── scheduled_collection.log
```

### File Naming Convention
- **Exports**: `us_exports_{product}_{year}_{month}.csv`
- **Imports**: `us_imports_{product}_from_{country}_{year}_{month}.csv`
- **Monthly Trends**: `monthly_{product}_imports_{year}_{month}.csv`

## 📊 Data Content

Each CSV file contains:

### Export Data Columns
- `E_COMMODITY`: HS code
- `E_COMMODITY_LDESC`: Product description
- `ALL_VAL_MO`: Monthly value
- `ALL_VAL_YR`: Year-to-date value
- `YEAR`: Data year
- `MONTH`: Data month

### Import Data Columns
- `CTY_CODE`: Country code
- `CTY_NAME`: Country name
- `GEN_VAL_MO`: General imports value (monthly)
- `CON_VAL_MO`: Consumption value (monthly)
- `E_COMMODITY`: HS code
- `E_COMMODITY_LDESC`: Product description
- `YEAR`: Data year
- `MONTH`: Data month

## 🛡 Error Handling

The system includes robust error handling:

- **API Failures**: Retries with exponential backoff
- **Network Issues**: Graceful degradation to cached data
- **File Errors**: Logging and continuation
- **Timeouts**: Configurable timeout settings

## 📈 Using the Data

### In the Dashboard
The Streamlit dashboard can access stored data for visualization:

```python
import pandas as pd

# Load coffee export data
coffee_data = pd.read_csv('data/census_data/us_exports_coffee_2023_12.csv')
```

### In Market Analysis
The MCP server can use stored data for trend analysis:

```python
# Compare current month with previous month
current_data = load_latest_data('coffee')
previous_data = load_previous_data('coffee')
trend = calculate_trend(current_data, previous_data)
```

## ⚙️ Configuration

### Adding New Products
1. Add to `AGRICULTURAL_PRODUCTS` dictionary in `automated_data_tracker.py`
2. Include HS code and product name
3. Run data collection to fetch new data

### Adding New Countries
1. Add to `AFRICAN_COUNTRIES` dictionary in `automated_data_tracker.py`
2. Include country name and Census code
3. Run data collection to fetch new data

### Adjusting Schedule
1. Modify scheduling in `scheduled_data_collection.py`
2. Update system task scheduler settings
3. Test new schedule

## 📚 Additional Resources

- [Census API Integration Guide](CENSUS_API_INTEGRATION_GUIDE.md)
- [U.S. Census Bureau International Trade Documentation](https://www.census.gov/data/developers/data-sets/international-trade.html)
- [Harmonized System (HS) Code Reference](https://www.census.gov/foreign-trade/schedules/b/2022/hs.pdf)

## 🆘 Troubleshooting

### Common Issues

1. **API Rate Limiting**
   - Solution: Increase delays between requests
   - Location: `time.sleep()` calls in data tracker

2. **Network Connectivity**
   - Solution: Check internet connection
   - Check: API endpoint availability

3. **File Permission Errors**
   - Solution: Verify write permissions on data directory
   - Location: `data/census_data/` directory

4. **Data Format Changes**
   - Solution: Update parsing logic
   - Location: Data handling functions in tracker script

### Log Files

- `data/tracking.log`: Detailed data collection logs
- `data/scheduled_collection.log`: Scheduled task logs

## 📞 Support

For questions about the automated data tracking system, contact:
- Terrence Dupree at Free World Trade Inc.
- Check the GitHub repository issues
- Review the documentation in this file

This automated system provides the foundation for continuous market intelligence to support your goal of becoming the #1 Africa-USA agriculture broker.