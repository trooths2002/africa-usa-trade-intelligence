import sys
import os

# Add the parent directory to the path to make relative imports work
# when running this script directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from typing import Dict, Any, Optional
import time
import uvicorn

# Try relative imports first, then absolute imports
try:
    from .data.collector import DataCollector
    from .intelligence.server import IntelligenceServer
    from .monitoring.health import HealthMonitor
except ImportError:
    # Fallback to absolute imports when running as script
    from data.collector import DataCollector
    from intelligence.server import IntelligenceServer
    from monitoring.health import HealthMonitor

app = FastAPI(title="Africa-USA Trade Intelligence API", version="1.0.0")

# Initialize services
data_collector = DataCollector()
intelligence_server = IntelligenceServer(data_collector)
health_monitor = HealthMonitor()

@app.get("/")
def read_root():
    return {"message": "Africa-USA Trade Intelligence API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return health_monitor.check_all_services()

@app.get("/census-data")
def get_census_data(trade_type: str = "imports", commodity_code: Optional[str] = None):
    return data_collector.get_census_data(trade_type, commodity_code)

@app.get("/exchange-rates")
def get_exchange_rates():
    return data_collector.get_exchange_rates()

@app.get("/commodity-prices")
def get_commodity_prices():
    return data_collector.get_commodity_prices()

@app.get("/trade-news")
def get_trade_news():
    return data_collector.get_trade_news()

@app.get("/african-markets")
def get_african_markets():
    """Get comprehensive African market intelligence"""
    return intelligence_server.get_african_market_intelligence()

@app.get("/custom-report")
def generate_custom_report(client_name: str, product_focus: str):
    """Generate a custom market analysis report"""
    client_profile = {"name": client_name}
    return intelligence_server.generate_custom_report(client_profile, product_focus)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)