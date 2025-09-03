#!/usr/bin/env python3
"""
Test CRM Models
Verify that CRM database models are correctly defined
"""
import sys
import os
import tempfile

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_crm_models():
    """
    Test that CRM models can be imported and instantiated
    """
    try:
        # Create a temporary database for testing
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_db.close()
        
        # Set up temporary database URL
        os.environ['DATABASE_URL'] = f'sqlite:///{temp_db.name}'
        
        # Import models
        from src.data.models.crm_models import (
            Supplier, Buyer, Lead, Quote, Shipment, Base
        )
        from sqlalchemy import create_engine
        
        # Create tables
        engine = create_engine(f'sqlite:///{temp_db.name}')
        Base.metadata.create_all(engine)
        
        print("✅ CRM models imported successfully")
        print("✅ CRM tables created successfully")
        
        # Clean up
        os.unlink(temp_db.name)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing CRM models: {e}")
        return False

def test_data_models():
    """
    Test that data ingestion models can be imported
    """
    try:
        # Create a temporary database for testing
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_db.close()
        
        # Set up temporary database URL
        os.environ['DATABASE_URL'] = f'sqlite:///{temp_db.name}'
        
        # Import and test data models
        from src.data.init_db import create_data_tables, create_arbitrage_tables
        from sqlalchemy import create_engine
        
        # Create tables
        engine = create_engine(f'sqlite:///{temp_db.name}')
        create_data_tables(engine)
        create_arbitrage_tables(engine)
        
        print("✅ Data ingestion models imported successfully")
        print("✅ Data tables created successfully")
        
        # Clean up
        os.unlink(temp_db.name)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data models: {e}")
        return False

def main():
    """
    Main test function
    """
    print("Testing CRM and Data Models...")
    print("=" * 40)
    
    success = True
    
    # Test CRM models
    print("\n1. Testing CRM Models...")
    if not test_crm_models():
        success = False
    
    # Test data models
    print("\n2. Testing Data Ingestion Models...")
    if not test_data_models():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All model tests passed!")
    else:
        print("❌ Some model tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)