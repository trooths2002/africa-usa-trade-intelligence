from sqlalchemy import create_engine, text
import os

# Use PostgreSQL database URL from environment or fallback to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trade_intelligence.db")
engine = create_engine(DATABASE_URL, future=True)


def init_db():
    """Initialize the user_state table if it doesn't exist."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_state (
                user_id TEXT PRIMARY KEY,
                saved_filters TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))


def save_user_state(user_id: str, filters: dict):
    """Persist user filters or state to the database.

    Args:
        user_id: Identifier for the user (e.g., email or username).
        filters: Dictionary containing the user's filter settings/state.
    """
    import json
    state_json = json.dumps(filters)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO user_state(user_id, saved_filters, updated_at)
                VALUES (:uid, :state, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    saved_filters = EXCLUDED.saved_filters,
                    updated_at = CURRENT_TIMESTAMP
                """
            ),
            {"uid": user_id, "state": state_json}
        )


def load_user_state(user_id: str) -> dict:
    """Retrieve persisted user state from the database.

    Args:
        user_id: Identifier for the user.

    Returns:
        A dictionary of the saved state, or an empty dict if none exists.
    """
    import json
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT saved_filters FROM user_state WHERE user_id = :uid"),
            {"uid": user_id}
        ).fetchone()
    if row and row[0]:
        try:
            return json.loads(row[0])
        except Exception:
            # Return empty dict if JSON decoding fails
            return {}
    return {}
