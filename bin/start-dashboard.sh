#!/usr/bin/env bash
set -euo pipefail

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

APP_ENTRY="${APP_ENTRY:-src/dashboard/app.py}"
# Streamlit needs these flags for container hosting
exec streamlit run "$APP_ENTRY" --server.port="${PORT:-8501}" --server.address="0.0.0.0"