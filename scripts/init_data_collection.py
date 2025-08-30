#!/usr/bin/env python3
"""
Initialize Data Collection System for Africa-USA Trade Intelligence
Sets up the automated data tracking system
"""

import os
import sys
import subprocess
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_data_directories():
    """Create necessary data directories"""
    logger.info("Setting up data directories...")
    
    directories = [
        "data",
        "data/census_data",
        "data/suppliers",
        "data/buyers",
        "data/market_intelligence"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def create_initial_data_files():
    """Create initial data files and tracking logs"""
    logger.info("Creating initial data files...")
    
    # Create tracking log files
    log_files = [
        "data/tracking.log",
        "data/scheduled_collection.log"
    ]
    
    for log_file in log_files:
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write(f"Data tracking log initialized on {datetime.now()}\n")
            logger.info(f"Created log file: {log_file}")

def run_initial_data_collection():
    """Run the initial data collection"""
    logger.info("Running initial data collection...")
    
    try:
        result = subprocess.run([
            sys.executable,
            "scripts/automated_data_tracker.py"
        ], capture_output=True, text=True, timeout=600)  # 10 minute timeout
        
        if result.returncode == 0:
            logger.info("Initial data collection completed successfully")
            logger.debug(f"Output: {result.stdout}")
            return True
        else:
            logger.error(f"Initial data collection failed with return code {result.returncode}")
            logger.error(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Initial data collection timed out")
        return False
    except Exception as e:
        logger.error(f"Error running initial data collection: {str(e)}")
        return False

def setup_scheduled_tasks():
    """Set up scheduled tasks for automated data collection"""
    logger.info("Setting up scheduled tasks...")
    
    # On Windows, we can use the Task Scheduler
    # For now, we'll just document how to set it up
    task_info = """
    
To set up automated data collection on Windows:

1. Open Task Scheduler (taskschd.msc)
2. Create a new task with the following settings:
   - General Tab:
     * Name: AfricaTradeDataCollection
     * Run whether user is logged on or not: Checked
   - Triggers Tab:
     * New Trigger: Daily at 2:00 AM
   - Actions Tab:
     * New Action:
       - Program/script: python
       - Add arguments: scripts/scheduled_data_collection.py
       - Start in: [Your project directory]
   - Conditions Tab:
     * Wake the computer to run this task: Checked
   - Settings Tab:
     * Allow task to be run on demand: Checked
     * If the task is not running, restart every: 1 minute
     * Stop the task if it runs longer than: 1 hour

Alternatively, you can run the scheduled collection script manually:
python scripts/scheduled_data_collection.py

"""
    
    # Save task info to a file
    with open("data/scheduled_task_setup.txt", "w") as f:
        f.write(task_info)
    
    logger.info("Scheduled task setup information saved to data/scheduled_task_setup.txt")

def main():
    """Main initialization function"""
    logger.info("=" * 60)
    logger.info("INITIALIZING DATA COLLECTION SYSTEM")
    logger.info("=" * 60)
    
    try:
        # Setup directories
        setup_data_directories()
        
        # Create initial files
        create_initial_data_files()
        
        # Setup scheduled tasks
        setup_scheduled_tasks()
        
        # Run initial data collection
        success = run_initial_data_collection()
        
        if success:
            logger.info("=" * 60)
            logger.info("DATA COLLECTION SYSTEM INITIALIZED SUCCESSFULLY")
            logger.info("Data will be automatically collected on a daily basis")
            logger.info("=" * 60)
        else:
            logger.warning("=" * 60)
            logger.warning("DATA COLLECTION SYSTEM INITIALIZED WITH WARNINGS")
            logger.warning("Initial data collection failed, but system is ready")
            logger.warning("You can run scripts/automated_data_tracker.py manually")
            logger.warning("=" * 60)
            
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()