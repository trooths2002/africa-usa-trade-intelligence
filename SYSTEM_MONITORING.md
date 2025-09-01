# System Monitoring and Automated Corrections

## Overview
This document describes the comprehensive monitoring system for the Africa-USA Trade Intelligence Platform that continuously monitors the dashboard and system components, automatically corrects issues, and provides hourly status updates to temangroup1930@gmail.com.

## Monitoring Components

### 1. Monitoring Agent
The core monitoring agent (`src/monitoring/agent.py`) performs the following functions:
- Checks API health and responsiveness
- Verifies dashboard accessibility
- Tests critical data endpoints
- Sends hourly email status updates
- Attempts automatic corrections for common issues
- Saves monitoring results for dashboard visualization

### 2. Dashboard Monitor
The dashboard monitor (`src/monitoring/dashboard_monitor.py`) provides more frequent checks:
- Verifies dashboard accessibility every 5 minutes
- Uses Selenium to test dashboard interactivity
- Checks API connectivity from the dashboard perspective
- Saves detailed results for troubleshooting

### 3. Monitoring Dashboard
The monitoring dashboard (`src/monitoring/dashboard.py`) provides a web interface to view:
- Real-time system status
- Historical monitoring data
- Health trends and metrics
- Data endpoint performance

## Automated Monitoring Schedule

### Hourly Monitoring (24/7)
- **Frequency**: Every hour, 24 hours a day
- **Duration**: Continuous for the next 7 days (configurable)
- **Actions**:
  - Full system health check
  - Email status update to temangroup1930@gmail.com
  - Automatic correction attempts for detected issues
  - Data persistence for dashboard visualization

### Dashboard Monitoring (Every 30 Minutes)
- **Frequency**: Every 30 minutes
- **Actions**:
  - Dashboard accessibility verification
  - Interactive element testing with Selenium
  - API connectivity verification
  - Detailed result logging

## Email Notifications

### Hourly Status Updates
- **Recipient**: temangroup1930@gmail.com
- **Content**:
  - Overall system health status
  - API status and response details
  - Dashboard accessibility status
  - Data endpoint performance metrics
  - System metrics and monitoring information

### Critical Alerts
- **Trigger**: 2 consecutive failures of any critical component
- **Content**:
  - Detailed error information
  - Automatic correction attempts
  - Immediate action recommendations

## Automatic Corrections

The system attempts to automatically correct common issues:
- API connectivity problems
- Dashboard accessibility issues
- Data endpoint failures
- Performance degradation

## Data Persistence

Monitoring results are saved to:
- `monitoring_results.json` - Agent monitoring results
- `dashboard_monitor_results.json` - Dashboard monitoring results

These files are used by the monitoring dashboard for visualization.

## Configuration

### Environment Variables
The monitoring system uses the following environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `STREAMLIT_API_URL` | API endpoint for health checks | https://africa-usa-trade-intelligence.onrender.com |
| `MONITORING_INTERVAL` | Seconds between checks | 3600 (1 hour) |
| `ALERT_THRESHOLD` | Consecutive failures before alert | 3 |
| `EMAIL_RECIPIENT` | Status report recipient | temangroup1930@gmail.com |
| `EMAIL_SENDER` | Sender email address | monitoring@africa-usa-trade.com |
| `EMAIL_PASSWORD` | Sender email password | (required for email) |
| `EMAIL_HOST` | SMTP server host | smtp.gmail.com |
| `EMAIL_PORT` | SMTP server port | 587 |
| `DASHBOARD_URL` | Dashboard URL for monitoring | http://localhost:8501 |
| `DASHBOARD_MONITOR_INTERVAL` | Dashboard check interval | 300 (5 minutes) |

## GitHub Actions Workflows

### Continuous Monitoring
- **File**: `.github/workflows/continuous-monitoring.yml`
- **Schedule**: Runs hourly for 7 days
- **Actions**: Executes monitoring agent and sends reports

### Dashboard Monitoring
- **File**: `.github/workflows/dashboard-monitoring.yml`
- **Schedule**: Runs every 30 minutes
- **Actions**: Executes dashboard monitor

### Monitoring Dashboard Deployment
- **File**: `.github/workflows/monitoring-dashboard.yml`
- **Trigger**: Changes to monitoring files
- **Actions**: Deploys monitoring dashboard

## Setup Instructions

### 1. Configure Email Notifications
To enable email notifications, set the following GitHub Secrets:
- `EMAIL_SENDER` - Your sender email address
- `EMAIL_PASSWORD` - Your sender email password or app-specific password

### 2. Configure URLs
Set the following GitHub Secrets if using custom URLs:
- `STREAMLIT_API_URL` - Your API endpoint
- `DASHBOARD_URL` - Your dashboard URL (if different from API)

### 3. Run Monitoring Locally
To run monitoring locally:
```bash
# Run the main monitoring agent
python src/monitoring/agent.py

# Run the dashboard monitor
python src/monitoring/dashboard_monitor.py
```

## Viewing Monitoring Results

### Web Dashboard
Access the monitoring dashboard at the designated URL to view:
- Real-time system status
- Historical monitoring data
- Health trends and performance metrics

### JSON Files
View raw monitoring data in:
- `monitoring_results.json` - Agent results
- `dashboard_monitor_results.json` - Dashboard monitor results

## Troubleshooting

### No Email Notifications
1. Verify `EMAIL_SENDER` and `EMAIL_PASSWORD` are configured
2. Check that the email account allows SMTP access
3. Verify the recipient email address is correct

### Monitoring Failures
1. Check GitHub Actions logs for error details
2. Verify all required dependencies are installed
3. Confirm network connectivity to monitored services

### Dashboard Issues
1. Ensure the dashboard is accessible at the configured URL
2. Check that Selenium WebDriver is properly installed
3. Verify Chrome/Chromium is available for Selenium tests

## Future Enhancements

### Advanced Monitoring
- Machine learning-based anomaly detection
- Predictive failure analysis
- Performance optimization recommendations

### Enhanced Notifications
- Slack/Teams integration
- SMS alerts for critical issues
- Custom notification rules

### Improved Auto-Correction
- Automated restart of failed services
- Dynamic scaling based on load
- Self-healing infrastructure

This monitoring system ensures that the Africa-USA Trade Intelligence Platform operates at peak performance with minimal manual intervention, automatically detecting and correcting issues while keeping stakeholders informed of system status.# System Monitoring and Automated Corrections

## Overview
This document describes the comprehensive monitoring system for the Africa-USA Trade Intelligence Platform that continuously monitors the dashboard and system components, automatically corrects issues, and provides hourly status updates to temangroup1930@gmail.com.

## Monitoring Components

### 1. Monitoring Agent
The core monitoring agent (`src/monitoring/agent.py`) performs the following functions:
- Checks API health and responsiveness
- Verifies dashboard accessibility
- Tests critical data endpoints
- Sends hourly email status updates
- Attempts automatic corrections for common issues
- Saves monitoring results for dashboard visualization

### 2. Dashboard Monitor
The dashboard monitor (`src/monitoring/dashboard_monitor.py`) provides more frequent checks:
- Verifies dashboard accessibility every 5 minutes
- Uses Selenium to test dashboard interactivity
- Checks API connectivity from the dashboard perspective
- Saves detailed results for troubleshooting

### 3. Monitoring Dashboard
The monitoring dashboard (`src/monitoring/dashboard.py`) provides a web interface to view:
- Real-time system status
- Historical monitoring data
- Health trends and metrics
- Data endpoint performance

## Automated Monitoring Schedule

### Hourly Monitoring (24/7)
- **Frequency**: Every hour, 24 hours a day
- **Duration**: Continuous for the next 7 days (configurable)
- **Actions**:
  - Full system health check
  - Email status update to temangroup1930@gmail.com
  - Automatic correction attempts for detected issues
  - Data persistence for dashboard visualization

### Dashboard Monitoring (Every 30 Minutes)
- **Frequency**: Every 30 minutes
- **Actions**:
  - Dashboard accessibility verification
  - Interactive element testing with Selenium
  - API connectivity verification
  - Detailed result logging

## Email Notifications

### Hourly Status Updates
- **Recipient**: temangroup1930@gmail.com
- **Content**:
  - Overall system health status
  - API status and response details
  - Dashboard accessibility status
  - Data endpoint performance metrics
  - System metrics and monitoring information

### Critical Alerts
- **Trigger**: 2 consecutive failures of any critical component
- **Content**:
  - Detailed error information
  - Automatic correction attempts
  - Immediate action recommendations

## Automatic Corrections

The system attempts to automatically correct common issues:
- API connectivity problems
- Dashboard accessibility issues
- Data endpoint failures
- Performance degradation

## Data Persistence

Monitoring results are saved to:
- `monitoring_results.json` - Agent monitoring results
- `dashboard_monitor_results.json` - Dashboard monitoring results

These files are used by the monitoring dashboard for visualization.

## Configuration

### Environment Variables
The monitoring system uses the following environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `STREAMLIT_API_URL` | API endpoint for health checks | https://africa-usa-trade-intelligence.onrender.com |
| `MONITORING_INTERVAL` | Seconds between checks | 3600 (1 hour) |
| `ALERT_THRESHOLD` | Consecutive failures before alert | 3 |
| `EMAIL_RECIPIENT` | Status report recipient | temangroup1930@gmail.com |
| `EMAIL_SENDER` | Sender email address | monitoring@africa-usa-trade.com |
| `EMAIL_PASSWORD` | Sender email password | (required for email) |
| `EMAIL_HOST` | SMTP server host | smtp.gmail.com |
| `EMAIL_PORT` | SMTP server port | 587 |
| `DASHBOARD_URL` | Dashboard URL for monitoring | http://localhost:8501 |
| `DASHBOARD_MONITOR_INTERVAL` | Dashboard check interval | 300 (5 minutes) |

## GitHub Actions Workflows

### Continuous Monitoring
- **File**: `.github/workflows/continuous-monitoring.yml`
- **Schedule**: Runs hourly for 7 days
- **Actions**: Executes monitoring agent and sends reports

### Dashboard Monitoring
- **File**: `.github/workflows/dashboard-monitoring.yml`
- **Schedule**: Runs every 30 minutes
- **Actions**: Executes dashboard monitor

### Monitoring Dashboard Deployment
- **File**: `.github/workflows/monitoring-dashboard.yml`
- **Trigger**: Changes to monitoring files
- **Actions**: Deploys monitoring dashboard

## Setup Instructions

### 1. Configure Email Notifications
To enable email notifications, set the following GitHub Secrets:
- `EMAIL_SENDER` - Your sender email address
- `EMAIL_PASSWORD` - Your sender email password or app-specific password

### 2. Configure URLs
Set the following GitHub Secrets if using custom URLs:
- `STREAMLIT_API_URL` - Your API endpoint
- `DASHBOARD_URL` - Your dashboard URL (if different from API)

### 3. Run Monitoring Locally
To run monitoring locally:
```bash
# Run the main monitoring agent
python src/monitoring/agent.py

# Run the dashboard monitor
python src/monitoring/dashboard_monitor.py
```

## Viewing Monitoring Results

### Web Dashboard
Access the monitoring dashboard at the designated URL to view:
- Real-time system status
- Historical monitoring data
- Health trends and performance metrics

### JSON Files
View raw monitoring data in:
- `monitoring_results.json` - Agent results
- `dashboard_monitor_results.json` - Dashboard monitor results

## Troubleshooting

### No Email Notifications
1. Verify `EMAIL_SENDER` and `EMAIL_PASSWORD` are configured
2. Check that the email account allows SMTP access
3. Verify the recipient email address is correct

### Monitoring Failures
1. Check GitHub Actions logs for error details
2. Verify all required dependencies are installed
3. Confirm network connectivity to monitored services

### Dashboard Issues
1. Ensure the dashboard is accessible at the configured URL
2. Check that Selenium WebDriver is properly installed
3. Verify Chrome/Chromium is available for Selenium tests

## Future Enhancements

### Advanced Monitoring
- Machine learning-based anomaly detection
- Predictive failure analysis
- Performance optimization recommendations

### Enhanced Notifications
- Slack/Teams integration
- SMS alerts for critical issues
- Custom notification rules

### Improved Auto-Correction
- Automated restart of failed services
- Dynamic scaling based on load
- Self-healing infrastructure

This monitoring system ensures that the Africa-USA Trade Intelligence Platform operates at peak performance with minimal manual intervention, automatically detecting and correcting issues while keeping stakeholders informed of system status.