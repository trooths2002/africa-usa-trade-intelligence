#!/usr/bin/env bash
set -euo pipefail

mkdir -p src/config src/health bin .github/workflows

cat > src/config/settings.py <<'PY'
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
PY

cat > src/health/main.py <<'PY'
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
PY

cat > bin/start-dashboard.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
APP_ENTRY="${APP_ENTRY:-src/dashboard/app.py}"
# Streamlit needs these flags for container hosting
exec streamlit run "$APP_ENTRY" --server.port="${PORT:-8501}" --server.address="0.0.0.0"
SH
chmod +x bin/start-dashboard.sh

cat > bin/start-health.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
# FastAPI health sidecar
exec uvicorn src.health.main:app --host 0.0.0.0 --port "${PORT:-8000}"
SH
chmod +x bin/start-health.sh

cat > render.yaml <<'YML'
services:
  - type: web
    name: ausa-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: bash bin/start-dashboard.sh
    plan: free
    envVars:
      - key: APP_LOGIN_PASSWORD
        sync: false
      - key: DATABASE_URL
        sync: false
      - key: STREAMLIT_API_URL
        sync: false

  - type: web
    name: ausa-health
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: bash bin/start-health.sh
    plan: free
YML

cat > Procfile <<'PROC'
web: bash bin/start-dashboard.sh
health: bash bin/start-health.sh
PROC

mkdir -p .github/workflows
cat > .github/workflows/health-check.yml <<'YML'
name: Health check
on:
  workflow_dispatch:
  schedule:
    - cron: "*/30 * * * *"  # every 30 min
jobs:
  probe:
    runs-on: ubuntu-latest
    env:
      STREAMLIT_API_URL: ${{ secrets.STREAMLIT_API_URL }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.10" }
      - run: pip install -r requirements.txt
      - name: Run dashboard probe
        run: |
          python - <<'PY'
          import os, sys, time, requests
          url = os.environ.get("STREAMLIT_API_URL")
          if not url:
              print("STREAMLIT_API_URL not set"); sys.exit(2)
          start = time.time()
          try:
              r = requests.get(url, timeout=15)
              dt = (time.time()-start)*1000
              print(f"{url} -> {r.status_code} in {dt:.0f}ms")
              sys.exit(0 if r.ok else 1)
          except Exception as e:
              print("Probe failed:", e); sys.exit(3)
          PY
YML

# Ensure requirements present
touch requirements.txt
for p in python-dotenv fastapi uvicorn httpx requests sqlalchemy psycopg2-binary streamlit; do
  grep -qi "^$p" requirements.txt || echo "$p" >> requirements.txt
done

git add -A
git commit -m "chore: add render/Procfile, health sidecar, CI probe, and runtime settings (Option A)"
echo "Config pack applied. Push this commit, set host env vars, and deploy."