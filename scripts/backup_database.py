#!/usr/bin/env python3
"""
Database backup script for Africa-USA Trade Intelligence Platform
"""

import os
import subprocess
import datetime
from src.config.settings import DATABASE_URL

def backup_database():
    """
    Create a backup of the PostgreSQL database
    """
    # Check if this is a PostgreSQL database
    if not DATABASE_URL.startswith("postgresql://"):
        print("This backup script is designed for PostgreSQL databases only")
        print("Current DATABASE_URL is not a PostgreSQL connection string")
        return False
    
    # Extract database connection details from DATABASE_URL
    # Format: postgresql://username:password@host:port/database
    try:
        # Parse the connection string
        parts = DATABASE_URL.replace("postgresql://", "").split("@")
        user_pass = parts[0].split(":")
        host_port_db = parts[1].split("/")
        
        username = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ""
        host_port = host_port_db[0].split(":")
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "5432"
        database = host_port_db[1]
        
        # Create backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"database_backup_{timestamp}.sql"
        
        # Set environment variable for password to avoid prompt
        env = os.environ.copy()
        if password:
            env["PGPASSWORD"] = password
        
        # Run pg_dump command
        cmd = [
            "pg_dump",
            "-h", host,
            "-p", port,
            "-U", username,
            "-d", database,
            "-f", backup_filename
        ]
        
        print(f"Creating database backup: {backup_filename}")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Database backup created successfully: {backup_filename}")
            # Show file size
            try:
                size = os.path.getsize(backup_filename)
                print(f"Backup file size: {size / 1024 / 1024:.2f} MB")
            except:
                pass
            return True
        else:
            print(f"✗ Database backup failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error parsing database connection string: {e}")
        return False

def schedule_weekly_backup():
    """
    Create a cron job for weekly database backups
    """
    # This function would typically be used in a production environment
    # to set up automatic weekly backups
    print("To schedule weekly backups, add this line to your crontab:")
    print("0 2 * * 0 /usr/bin/python3 /path/to/backup_database.py")
    print("(This runs the backup every Sunday at 2 AM)")

if __name__ == "__main__":
    if backup_database():
        print("\n✅ Database backup completed successfully!")
    else:
        print("\n❌ Database backup failed!")
        exit(1)