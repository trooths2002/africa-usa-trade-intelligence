#!/usr/bin/env python3
"""
Database initialization script for production deployment
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def init_production_database():
    """
    Initialize the production database
    """
    try:
        from data.init_db import init_database
        print("Initializing production database...")
        init_database()
        print("✅ Database initialization completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    if init_production_database():
        sys.exit(0)
    else:
        sys.exit(1)