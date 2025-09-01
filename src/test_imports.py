#!/usr/bin/env python3
"""
Test script to verify that all modules can be imported correctly
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        # Test data collector import
        from data.collector import DataCollector
        print("✅ DataCollector import successful")
        
        # Test intelligence server import
        from intelligence.server import IntelligenceServer
        print("✅ IntelligenceServer import successful")
        
        # Test health monitor import
        from monitoring.health import HealthMonitor
        print("✅ HealthMonitor import successful")
        
        # Test API imports
        from api.main import app
        print("✅ FastAPI app import successful")
        
        # Test that we can instantiate the classes
        data_collector = DataCollector()
        print("✅ DataCollector instantiation successful")
        
        intelligence_server = IntelligenceServer(data_collector)
        print("✅ IntelligenceServer instantiation successful")
        
        health_monitor = HealthMonitor()
        print("✅ HealthMonitor instantiation successful")
        
        print("\n🎉 All imports and instantiations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)