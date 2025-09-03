import os
from dotenv import load_dotenv

# Load .env if present (local dev). No dependency on .env in prod.
load_dotenv()

APP_LOGIN_PASSWORD = os.getenv("APP_LOGIN_PASSWORD", "change-me-dev")
DATABASE_URL       = os.getenv("DATABASE_URL", "sqlite:///./trade_intelligence.db")
STREAMLIT_API_URL  = os.getenv("STREAMLIT_API_URL", "http://localhost:8501")
DEFAULT_USER_ID    = os.getenv("DEFAULT_USER_ID", "terrence@freeworldtrade")

def summarize():
    return {
        "APP_LOGIN_PASSWORD_set": bool(os.getenv("APP_LOGIN_PASSWORD")),
        "DATABASE_URL": DATABASE_URL,
        "STREAMLIT_API_URL": STREAMLIT_API_URL,
        "DEFAULT_USER_ID": DEFAULT_USER_ID,
    }