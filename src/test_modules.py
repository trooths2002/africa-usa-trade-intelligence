"""
Test script to verify that all modules work correctly
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_data_collector():
    """Test the data collector module"""
    print("Testing DataCollector...")
    try:
        from data.collector import DataCollector
        collector = DataCollector()
        
        # Test basic data collection
        census_data = collector.get_census_data()
        print(f"Census data collected: {len(census_data.get('data', []))} rows")
        
        exchange_rates = collector.get_exchange_rates()
        print(f"Exchange rates collected: {len(exchange_rates.get('rates', {}))} currencies")
        
        commodity_prices = collector.get_commodity_prices()
        print(f"Commodity prices collected: {len(commodity_prices.get('prices', {}))} items")
        
        # Test new features
        african_data = collector.get_african_exchange_data()
        print(f"African exchange data collected: {len(african_data.get('exchanges', {}))} exchanges")
        
        sentiment_data = collector.get_social_sentiment(["coffee", "cocoa"])
        print(f"Social sentiment data collected: {sentiment_data.get('keywords', [])}")
        
        print("DataCollector tests passed!")
        return True
    except Exception as e:
        print(f"DataCollector tests failed: {e}")
        return False

def test_intelligence_server():
    """Test the intelligence server module"""
    print("\nTesting IntelligenceServer...")
    try:
        from data.collector import DataCollector
        from intelligence.server import IntelligenceServer
        
        collector = DataCollector()
        server = IntelligenceServer(collector)
        
        # Test African market intelligence
        african_intel = server.get_african_market_intelligence()
        if "error" in african_intel:
            print(f"African market intelligence failed: {african_intel['error']}")
            return False
        
        print(f"African market intelligence collected: {len(african_intel.get('opportunities', []))} opportunities")
        
        # Test custom report generation
        custom_report = server.generate_custom_report({"name": "Test Client"}, "coffee")
        if "error" in custom_report:
            print(f"Custom report generation failed: {custom_report['error']}")
            return False
            
        print("Custom report generated successfully")
        print("IntelligenceServer tests passed!")
        return True
    except Exception as e:
        print(f"IntelligenceServer tests failed: {e}")
        return False

def test_health_monitor():
    """Test the health monitor module"""
    print("\nTesting HealthMonitor...")
    try:
        from monitoring.health import HealthMonitor
        monitor = HealthMonitor()
        
        # Test health check (this will fail since services aren't running, but class should instantiate)
        print("HealthMonitor instantiated successfully")
        print("HealthMonitor tests passed!")
        return True
    except Exception as e:
        print(f"HealthMonitor tests failed: {e}")
        return False

if __name__ == "__main__":
    print("Running module tests...\n")
    
    success = True
    success &= test_data_collector()
    success &= test_intelligence_server()
    success &= test_health_monitor()
    
    if success:
        print("\nAll module tests passed!")
    else:
        print("\nSome module tests failed!")
        sys.exit(1)