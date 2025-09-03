#!/usr/bin/env bash
set -euo pipefail
# FastAPI health sidecar
exec uvicorn src.health.main:app --host 0.0.0.0 --port "${PORT:-8000}"