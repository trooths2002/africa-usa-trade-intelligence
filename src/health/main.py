from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trade_intelligence.db")

@app.get("/health")
def health():
    """
    Health check endpoint that verifies:
    1. Service is running
    2. Database connectivity
    3. Data freshness (if tables exist)
    """
    try:
        # Check database connectivity
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            db_status = "ok" if result.fetchone() else "error"
        
        # Try to check data freshness if tables exist
        freshness_info = {}
        try:
            with engine.connect() as conn:
                # Check if census_data table exists and get last entry
                try:
                    result = conn.execute(text("SELECT MAX(timestamp) as last_updated FROM census_data"))
                    row = result.fetchone()
                    if row and row[0]:
                        last_updated = row[0]
                        if isinstance(last_updated, str):
                            # If it's a string, parse it
                            from datetime import datetime
                            last_updated = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                        hours_since_update = (datetime.now() - last_updated).total_seconds() / 3600
                        freshness_info["census_data_hours"] = round(hours_since_update, 1)
                except Exception as e:
                    logger.debug(f"Could not check census_data freshness: {e}")
                
                # Check if world_bank_data table exists and get last entry
                try:
                    result = conn.execute(text("SELECT MAX(timestamp) as last_updated FROM world_bank_data"))
                    row = result.fetchone()
                    if row and row[0]:
                        last_updated = row[0]
                        if isinstance(last_updated, str):
                            # If it's a string, parse it
                            from datetime import datetime
                            last_updated = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                        hours_since_update = (datetime.now() - last_updated).total_seconds() / 3600
                        freshness_info["world_bank_data_hours"] = round(hours_since_update, 1)
                except Exception as e:
                    logger.debug(f"Could not check world_bank_data freshness: {e}")
        except Exception as e:
            logger.debug(f"Could not check data freshness: {e}")
        
        response = {
            "status": "healthy",
            "timestamp": datetime.now().timestamp(),
            "service": "Africa-USA Trade Intelligence Platform",
            "database": db_status
        }
        
        # Add freshness info if available
        if freshness_info:
            response.update(freshness_info)
        
        return response
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().timestamp(),
            "service": "Africa-USA Trade Intelligence Platform",
            "error": str(e)
        }