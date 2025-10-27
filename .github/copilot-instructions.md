# Africa-USA Trade Intelligence Platform

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap, Build, and Test the Repository
- Create and activate virtual environment:
  - `python -m venv venv`
  - Linux/Mac: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- Install dependencies:
  - `pip install --upgrade pip`
  - `pip install -r requirements.txt` -- EXPECTED TO FAIL due to network timeout issues in current environment
  - **ALTERNATIVE**: `pip install fastapi uvicorn streamlit pandas requests beautifulsoup4 python-dotenv` -- Core packages that work. Takes 2-3 minutes. NEVER CANCEL.
- Setup environment configuration:
  - `cp .env.example .env`
  - Edit .env with free API keys (see validation steps below)
- Initialize and test the platform:
  - `python setup.py` -- This runs the automated setup script but requires setuptools packages
  - Alternative manual setup: Create basic directory structure if missing

### Running the Applications
- **API Server**: 
  - `python -m uvicorn src_clean.api.main:app --host 0.0.0.0 --port 8000`
  - Access at http://localhost:8000
  - API docs at http://localhost:8000/docs
  - Takes 5-10 seconds to start. NEVER CANCEL before 30 seconds.
- **Streamlit Dashboard**: 
  - `python -m streamlit run src_clean/dashboard/app.py --server.port 8501`
  - Access at http://localhost:8501
  - Takes 10-15 seconds to start. NEVER CANCEL before 45 seconds.
- **All Services Together**: 
  - `python src_clean/main.py` -- Launches API, MCP server, and dashboard together
  - Takes 30-45 seconds to fully start all services. NEVER CANCEL before 90 seconds.

### Testing and Validation
- Basic functionality test: `python -c "import fastapi, uvicorn, streamlit, pandas, requests; print('✅ Core packages working')"`
- API health check: `curl http://localhost:8000/health`
- Test specific endpoints: 
  - `curl http://localhost:8000/exchange-rates`
  - `curl http://localhost:8000/commodity-prices`
  - `curl http://localhost:8000/census/imports/0901`
- Run comprehensive tests: `python scripts/run_free_api_tests.py` -- Takes 30-60 seconds. NEVER CANCEL.
- Run simple API validation: `python scripts/validate_free_apis.py` -- Takes 15-30 seconds. NEVER CANCEL.
- Census API test: `python scripts/test_census_api.py` -- May fail due to network restrictions but provides examples

## Validation

### **CRITICAL**: Manual Validation Scenarios
After making changes, ALWAYS test these complete user scenarios:

1. **API Functionality Test**:
   - Start API server: `python -m uvicorn src_clean.api.main:app --host 0.0.0.0 --port 8000`
   - Wait 30 seconds for startup. NEVER CANCEL.
   - Test health: `curl http://localhost:8000/health`
   - Test data endpoints: `curl http://localhost:8000/exchange-rates`
   - Verify JSON responses contain expected data structure

2. **Dashboard Complete Test**:
   - Start dashboard: `python -m streamlit run src_clean/dashboard/app.py --server.port 8501`
   - Wait 45 seconds for startup. NEVER CANCEL.
   - Access http://localhost:8501 in browser if available
   - Verify dashboard loads without Python errors in logs
   - Check that API connectivity status shows in dashboard

3. **Full Platform Integration Test**:
   - Start all services: `python src_clean/main.py`
   - Wait 90 seconds for complete startup. NEVER CANCEL.
   - Test API endpoints still respond
   - Verify dashboard can connect to local API
   - Test end-to-end data flow from API to dashboard

### Build and Package Requirements Issues
- **CRITICAL**: `pip install -r requirements.txt` FAILS due to network timeouts in current environment
- **WORKAROUND**: Install core packages individually: `pip install fastapi uvicorn streamlit pandas requests beautifulsoup4 python-dotenv`
- **BUILD TIME**: Core package installation takes 2-4 minutes. NEVER CANCEL. Set timeout to 10+ minutes.
- **MCP Package**: `pip install mcp` may fail - this is acceptable for basic functionality
- **Testing packages**: `pytest`, `feedparser` may fail to install - use alternative validation methods

### Expected Timing and Timeouts
- **Virtual environment creation**: 10-30 seconds. Set timeout to 60 seconds.
- **Core package installation**: 2-4 minutes. NEVER CANCEL. Set timeout to 10+ minutes.
- **Full requirements.txt**: EXPECTED TO FAIL due to network issues. Do not attempt.
- **API server startup**: 5-10 seconds. NEVER CANCEL before 30 seconds.
- **Streamlit startup**: 10-15 seconds. NEVER CANCEL before 45 seconds.
- **All services startup**: 30-45 seconds. NEVER CANCEL before 90 seconds.

## Common Tasks

### Key Projects in This Codebase
1. **src_clean/** - Main clean architecture implementation
   - `api/main.py` - FastAPI server with caching
   - `dashboard/app.py` - Streamlit dashboard
   - `main.py` - Service launcher
   - `config.py` - Configuration management

2. **src/** - Alternative implementation (similar structure)
3. **scripts/** - Testing and validation utilities
   - `run_free_api_tests.py` - Comprehensive test suite
   - `validate_free_apis.py` - Simple API validation
   - `test_census_api.py` - Census Bureau API examples
4. **tests/** - Test files (`test_free_apis.py`)

### Free API Integration Status
The platform uses 100% free APIs:
- **US Census Bureau API** - Trade data (may fail due to network restrictions)
- **Sample data fallbacks** - When real APIs unavailable
- **Exchange rate simulation** - Built-in sample rates
- **Commodity price simulation** - Built-in sample prices
- **RSS news feeds** - Free news sources (requires feedparser package)

### Repository Structure Quick Reference
```
africa-usa-trade-intelligence/
├── README.md
├── requirements.txt          # Full requirements (FAILS to install)
├── setup.py                 # Automated setup script
├── .env.example             # Environment template
├── src_clean/               # PRIMARY codebase
│   ├── api/main.py          # FastAPI server
│   ├── dashboard/app.py     # Streamlit dashboard
│   ├── main.py              # Service launcher
│   ├── requirements.txt     # Minimal working requirements
│   └── config.py            # Configuration
├── src/                     # Alternative implementation
├── scripts/                 # Testing utilities
│   ├── run_free_api_tests.py
│   ├── validate_free_apis.py
│   └── test_census_api.py
├── tests/
│   └── test_free_apis.py
└── .github/
    └── workflows/ci.yml     # GitHub Actions CI
```

### Environment Configuration
1. Copy environment template: `cp .env.example .env`
2. Edit .env file with these free API keys:
   - US Census Bureau API (optional): https://api.census.gov
   - World Bank API (no key required): https://api.worldbank.org
   - ExchangeRate.host (no key required): https://exchangerate.host
3. All external APIs are free-tier or no-cost services
4. Platform works with sample data when external APIs unavailable

### Development Workflow
- Always activate virtual environment first: `source venv/bin/activate`
- Use `src_clean/` as the primary codebase for development
- Test changes with: `python -m uvicorn src_clean.api.main:app --host 0.0.0.0 --port 8000`
- Validate dashboard with: `python -m streamlit run src_clean/dashboard/app.py --server.port 8501`
- Run validation suite: `python scripts/validate_free_apis.py`

### CI/CD Information
- GitHub Actions workflow: `.github/workflows/ci.yml`
- Runs Python 3.10 and 3.11 tests
- Uses ruff for linting: `ruff check .`
- Runs pytest: `pytest -q`
- Includes security scanning: `pip-audit`

## Important Notes
- This is a trade intelligence platform for Africa-USA agricultural trade
- Designed to use 100% free resources and APIs
- Network connectivity issues may prevent full package installation
- Platform gracefully handles API failures with sample data
- Focus on src_clean/ directory for most development work
- Always test both API and dashboard after changes
- Allow adequate time for service startup - never cancel prematurely

## Commands That Don't Work
- `pip install -r requirements.txt` -- Network timeout issues
- External API calls may fail due to network restrictions
- `python setup.py` (as setup command) -- Use `python setup.py build` or similar with proper arguments
- MCP server components may not be fully testable due to missing dependencies

## Commands That Do Work
- `pip install fastapi uvicorn streamlit pandas requests beautifulsoup4 python-dotenv`
- `python -m uvicorn src_clean.api.main:app --host 0.0.0.0 --port 8000`
- `python -m streamlit run src_clean/dashboard/app.py --server.port 8501`
- `python src_clean/main.py`
- `curl http://localhost:8000/health`
- `python scripts/validate_free_apis.py`