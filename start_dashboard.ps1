# PowerShell script to start the Africa-USA Trade Intelligence Dashboard
# This script will start the Streamlit dashboard and open it in the default browser

Write-Host "🌍 Starting Africa-USA Trade Intelligence Dashboard..." -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $ScriptDir

Write-Host "📁 Working directory: $ScriptDir" -ForegroundColor Yellow

# Check if required files exist
$DashboardFile = "src\web_app\dashboard\main.py"
$RequirementsFile = "requirements.txt"

if (-Not (Test-Path $DashboardFile)) {
    Write-Host "❌ Error: Dashboard file not found at $DashboardFile" -ForegroundColor Red
    Write-Host "Please make sure you're running this script from the project root directory." -ForegroundColor Red
    Pause
    Exit 1
}

if (-Not (Test-Path $RequirementsFile)) {
    Write-Host "❌ Error: Requirements file not found at $RequirementsFile" -ForegroundColor Red
    Write-Host "Please make sure you're running this script from the project root directory." -ForegroundColor Red
    Pause
    Exit 1
}

Write-Host "✅ Required files found." -ForegroundColor Green

# Check if Python is installed
try {
    $PythonVersion = & python --version 2>&1
    Write-Host "✅ Python is available: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and make sure it's in your system PATH." -ForegroundColor Red
    Pause
    Exit 1
}

# Check if Streamlit is installed
try {
    $StreamlitVersion = & python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')"
    Write-Host "✅ $StreamlitVersion is available" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Streamlit not found. Installing required packages..." -ForegroundColor Yellow
    try {
        & pip install -r $RequirementsFile
        Write-Host "✅ Required packages installed successfully." -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: Failed to install required packages." -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Pause
        Exit 1
    }
}

# Start the dashboard
Write-Host "🚀 Starting dashboard server..." -ForegroundColor Cyan
Write-Host "The dashboard will be available at http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Cyan

try {
    & python -m streamlit run $DashboardFile --server.port 8501
} catch {
    Write-Host "❌ Error: Failed to start the dashboard." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Pause
    Exit 1
}