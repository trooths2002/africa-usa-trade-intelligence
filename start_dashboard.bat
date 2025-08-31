@echo off
title Africa-USA Trade Intelligence Dashboard

echo 🌍 Starting Africa-USA Trade Intelligence Dashboard...
echo ===========================================

REM Get the script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo 📁 Working directory: %SCRIPT_DIR%

REM Check if required files exist
set DASHBOARD_FILE=src\web_app\dashboard\main.py
set REQUIREMENTS_FILE=requirements.txt

if not exist "%DASHBOARD_FILE%" (
    echo ❌ Error: Dashboard file not found at %DASHBOARD_FILE%
    echo Please make sure you're running this script from the project root directory.
    pause
    exit /b 1
)

if not exist "%REQUIREMENTS_FILE%" (
    echo ❌ Error: Requirements file not found at %REQUIREMENTS_FILE%
    echo Please make sure you're running this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ Required files found.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH.
    echo Please install Python 3.8+ and make sure it's in your system PATH.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ Python is available: %PYTHON_VERSION%
)

REM Check if Streamlit is installed
python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Streamlit not found. Installing required packages...
    pip install -r "%REQUIREMENTS_FILE%"
    if %errorlevel% neq 0 (
        echo ❌ Error: Failed to install required packages.
        pause
        exit /b 1
    ) else (
        echo ✅ Required packages installed successfully.
    )
) else (
    for /f "tokens=*" %%i in ('python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')"'') do set STREAMLIT_VERSION=%%i
    echo ✅ %STREAMLIT_VERSION% is available
)

REM Start the dashboard
echo 🚀 Starting dashboard server...
echo The dashboard will be available at http://localhost:8501
echo Press Ctrl+C to stop the server.

python -m streamlit run "%DASHBOARD_FILE%" --server.port 8501

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to start the dashboard.
    pause
    exit /b 1
)