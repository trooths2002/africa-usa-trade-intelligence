#!/usr/bin/env python3
"""
Scheduled Data Collection for Africa-USA Trade Intelligence
Runs the automated data tracker on a regular schedule
"""

import os
import sys
import time
import logging
from datetime import datetime, timedelta
import subprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/scheduled_collection.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_data_tracker():
    """Run the automated data tracker script"""
    try:
        logger.info("Starting automated data tracker...")
        result = subprocess.run([
            sys.executable, 
            "scripts/automated_data_tracker.py"
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            logger.info("Data tracker completed successfully")
            logger.debug(f"Output: {result.stdout}")
        else:
            logger.error(f"Data tracker failed with return code {result.returncode}")
            logger.error(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("Data tracker timed out")
    except Exception as e:
        logger.error(f"Error running data tracker: {str(e)}")

def main():
    """Main function to schedule data collection"""
    logger.info("=" * 60)
    logger.info("SCHEDULED DATA COLLECTION STARTING")
    logger.info("=" * 60)
    
    # For demonstration, we'll run once immediately
    logger.info("Running initial data collection...")
    run_data_tracker()
    
    # In a production environment, you would schedule this to run regularly
    # For example, daily at 2 AM:
    # 
    # import schedule
    # 
    # schedule.every().day.at("02:00").do(run_data_tracker)
    # 
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
    
    logger.info("Scheduled data collection initialized")
    logger.info("To set up automatic daily collection, uncomment the schedule section")

if __name__ == "__main__":
    main()