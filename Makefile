# Makefile for Africa-USA Trade Intelligence Platform

# Default target
.PHONY: help
help:
	@echo "Africa-USA Trade Intelligence Platform - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  setup         - Install package in development mode"
	@echo "  install       - Install package in development mode"
	@echo "  initdb        - Initialize database"
	@echo "  migrate       - Run database migrations"
	@echo "  migrate-init  - Initialize migrations"
	@echo "  ingest-census - Run Census data ingestion"
	@echo "  ingest-fred   - Run FRED data ingestion"
	@echo "  ingest-wb     - Run World Bank data ingestion"
	@echo "  fx-rates      - Run FX rates ingestion"
	@echo "  arbitrage     - Calculate arbitrage opportunities"
	@echo "  all-data      - Run all data ingestion jobs"
	@echo "  test          - Run tests"
	@echo "  lint          - Run code linting"
	@echo "  health        - Check service health"

# Setup and installation
.PHONY: setup install
setup install:
	pip install -e .

# Database initialization and migrations
.PHONY: initdb
initdb:
	python scripts/init_production_db.py

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: migrate-init
migrate-init:
	alembic revision --autogenerate -m "Auto-generated migration"

# Data ingestion jobs
.PHONY: ingest-census
ingest-census:
	ingest-census

.PHONY: ingest-fred
ingest-fred:
	ingest-fred

.PHONY: ingest-wb
ingest-wb:
	ingest-wb

.PHONY: fx-rates
fx-rates:
	fx-rates

.PHONY: arbitrage
arbitrage:
	refresh-arbitrage

.PHONY: all-data
all-data: ingest-census ingest-wb ingest-fred fx-rates arbitrage

# Testing and quality checks
.PHONY: test
test:
	python -m pytest tests/

.PHONY: lint
lint:
	ruff check .

# Health check
.PHONY: health
health:
	@echo "Checking health endpoint..."
	@python -c "import requests, os; url = os.environ.get('HEALTH_API_URL', 'http://localhost:8000'); r = requests.get(f'{url}/health', timeout=15); print(f'Status: {r.status_code}'); print(f'Response: {r.json()}')" || echo "Health check failed"