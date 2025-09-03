import os
from dotenv import load_dotenv

# Load .env if present (local dev). No dependency on .env in prod.
load_dotenv()

APP_LOGIN_PASSWORD = os.getenv("APP_LOGIN_PASSWORD", "change-me-dev")
DATABASE_URL       = os.getenv("DATABASE_URL", "sqlite:///./trade_intelligence.db")
DASHBOARD_URL      = os.getenv("DASHBOARD_URL", "http://localhost:8501")
API_BASE_URL       = os.getenv("API_BASE_URL", "http://localhost:8000")
HEALTH_API_URL     = os.getenv("HEALTH_API_URL", "http://localhost:8000")
DEFAULT_USER_ID    = os.getenv("DEFAULT_USER_ID", "terrence@freeworldtrade")

# Backward compatibility
STREAMLIT_API_URL  = os.getenv("STREAMLIT_API_URL", "http://localhost:8501")


def summarize():
    return {
        "APP_LOGIN_PASSWORD_set": bool(os.getenv("APP_LOGIN_PASSWORD")),
        "DATABASE_URL": DATABASE_URL,
        "DASHBOARD_URL": DASHBOARD_URL,
        "API_BASE_URL": API_BASE_URL,
        "HEALTH_API_URL": HEALTH_API_URL,
        "DEFAULT_USER_ID": DEFAULT_USER_ID,
    }