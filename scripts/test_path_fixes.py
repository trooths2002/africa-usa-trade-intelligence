#!/usr/bin/env python3
"""
Test script to verify that path fixes work correctly for importing modules
"""
import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

def test_imports():
    """Test that we can import all the necessary modules"""
    try:
        # Test importing from src.data.collector directly
        from data.collector import DataCollector
        print("✅ Successfully imported data.collector")
        
        # Test importing from src.intelligence.server
        from intelligence.server import IntelligenceServer
        print("✅ Successfully imported intelligence.server")
        
        # Test creating instances
        collector = DataCollector()
        print("✅ Successfully created DataCollector instance")
        
        server = IntelligenceServer(collector)
        print("✅ Successfully created IntelligenceServer instance")
        
        print("\n🎉 All imports and instantiations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error during imports: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing path fixes for module imports...")
    print(f"Python path: {sys.path[:3]}")  # Show first 3 paths for debugging
    success = test_imports()
    sys.exit(0 if success else 1)