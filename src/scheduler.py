#!/usr/bin/env python3
"""
Task Scheduler for Africa-USA Trade Intelligence Platform
Schedule and run data ingestion jobs, arbitrage calculations, and other periodic tasks
"""
import time
import schedule
import threading
from datetime import datetime
from data.jobs.ingestion_census import main as run_census_ingestion
from data.jobs.ingestion_wb import main as run_world_bank_ingestion
from data.jobs.ingestion_fred import main as run_fred_ingestion
from data.jobs.fx_rates import main as run_fx_rates_ingestion
from data.jobs.refresh_arbitrage import main as run_arbitrage_calculation

def run_scheduler():
    """
    Run the task scheduler
    """
    print("Starting task scheduler...")
    
    # Schedule jobs
    # Run data ingestion jobs daily at 2 AM
    schedule.every().day.at("02:00").do(run_census_ingestion)
    schedule.every().day.at("02:30").do(run_world_bank_ingestion)
    schedule.every().day.at("03:00").do(run_fred_ingestion)
    schedule.every().day.at("03:30").do(run_fx_rates_ingestion)
    
    # Run arbitrage calculation daily at 4 AM
    schedule.every().day.at("04:00").do(run_arbitrage_calculation)
    
    # Run FX rates update every 6 hours
    schedule.every(6).hours.do(run_fx_rates_ingestion)
    
    # Run a quick arbitrage check every hour during business hours
    schedule.every().hour.do(run_arbitrage_calculation)
    
    print("Scheduler started with the following jobs:")
    print("- Census data ingestion: Daily at 2:00 AM")
    print("- World Bank data ingestion: Daily at 2:30 AM")
    print("- FRED data ingestion: Daily at 3:00 AM")
    print("- FX rates update: Daily at 3:30 AM and every 6 hours")
    print("- Arbitrage calculation: Daily at 4:00 AM and every hour")
    
    # Run scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler_loop)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    return scheduler_thread

def scheduler_loop():
    """
    Main scheduler loop
    """
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def run_all_jobs_now():
    """
    Run all jobs immediately (for testing)
    """
    print(f"Running all jobs immediately at {datetime.now()}")
    
    print("Running Census data ingestion...")
    run_census_ingestion()
    
    print("Running World Bank data ingestion...")
    run_world_bank_ingestion()
    
    print("Running FRED data ingestion...")
    run_fred_ingestion()
    
    print("Running FX rates update...")
    run_fx_rates_ingestion()
    
    print("Running arbitrage calculation...")
    run_arbitrage_calculation()
    
    print("All jobs completed!")

if __name__ == "__main__":
    # For testing, run all jobs immediately
    run_all_jobs_now()
    
    # Then start the scheduler
    # scheduler_thread = run_scheduler()
    
    # Keep the main thread alive
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("Scheduler stopped by user")