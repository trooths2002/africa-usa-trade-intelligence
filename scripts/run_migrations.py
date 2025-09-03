#!/usr/bin/env python3
"""
Script to run database migrations
"""
import os
import subprocess
import sys

def run_migrations():
    """
    Run Alembic database migrations
    """
    try:
        print("Running database migrations...")
        result = subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrations completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running database migrations: {e}")
        return False
    except FileNotFoundError:
        print("Error: alembic command not found. Please install alembic:")
        print("  pip install alembic")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)