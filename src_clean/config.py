"""
Configuration for the Africa-USA Trade Intelligence Platform
"""
import os
from typing import Optional

class Config:
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Dashboard Configuration
    DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8501"))
    
    # Data Collection Configuration
    CACHE_EXPIRY_MINUTES = int(os.getenv("CACHE_EXPIRY_MINUTES", "30"))
    
    # External API Keys (all free services)
    CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", "")  # Census API doesn't require a key
    WORLD_BANK_API_URL = os.getenv("WORLD_BANK_API_URL", "https://api.worldbank.org/v2")
    
    # Monitoring Configuration
    HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "60"))  # seconds

config = Config()