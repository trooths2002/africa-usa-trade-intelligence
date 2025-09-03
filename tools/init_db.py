#!/usr/bin/env python3
"""
Database Initialization Tool
Initialize all database tables for the Africa-USA Trade Intelligence Platform
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """
    Main function to initialize the database
    """
    print("Initializing Africa-USA Trade Intelligence Platform Database...")
    
    try:
        # Import and run database initialization
        from src.data.init_db import init_database
        init_database()
        
        print("\n✅ Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Verify tables were created by checking your database")
        print("2. Run data ingestion jobs to populate initial data:")
        print("   - python src/data/jobs/ingestion_census.py")
        print("   - python src/data/jobs/ingestion_wb.py")
        print("   - python src/data/jobs/ingestion_fred.py")
        print("   - python src/data/jobs/fx_rates.py")
        print("3. Calculate initial arbitrage opportunities:")
        print("   - python src/data/jobs/refresh_arbitrage.py")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()