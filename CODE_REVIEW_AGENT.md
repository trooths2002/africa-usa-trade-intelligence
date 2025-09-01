# Automated Code Review Agent Configuration

## Purpose
This document defines the rules and guidelines for the automated code review agent that continuously improves the Africa-USA Trade Intelligence Platform.

## Review Criteria

### 1. Code Quality Standards
- All Python code must follow PEP 8 style guidelines
- Functions should be no longer than 50 lines
- Classes should have clear docstrings explaining their purpose
- Variable names should be descriptive and follow snake_case convention
- No unused imports or variables

### 2. Performance Optimization
- API calls should have appropriate timeout values
- Error handling should be comprehensive but not overly verbose
- Data fetching should be cached when appropriate
- Memory usage should be optimized for large datasets

### 3. Security Best Practices
- No hardcoded API keys or sensitive information
- Environment variables should be used for configuration
- Input validation should be performed on all user inputs
- Rate limiting should be implemented for external API calls

### 4. User Experience
- Error messages should be user-friendly and actionable
- Loading states should be shown during long operations
- Responsive design should work on different screen sizes
- Accessibility features should be implemented

### 5. Robustness
- All API calls should have proper error handling
- Fallback mechanisms should be in place for critical features
- Connection timeouts should be handled gracefully
- Retry mechanisms should be implemented for transient failures

## Automated Improvement Areas

### 1. Dashboard Enhancements
- Add more visualizations for trade data
- Implement real-time data updates
- Add export functionality for reports
- Improve mobile responsiveness

### 2. API Integration
- Add more data sources for comprehensive market intelligence
- Implement caching for frequently accessed data
- Add rate limiting to prevent API abuse
- Improve error handling for different API response types

### 3. Reporting Features
- Add customizable report templates
- Implement scheduled report generation
- Add export to PDF/Excel functionality
- Include historical data comparisons

### 4. User Management
- Add user authentication and authorization
- Implement role-based access control
- Add user preferences and customization
- Include audit logging for compliance

## Implementation Guidelines

### 1. Change Management
- All changes should be made in feature branches
- Pull requests should include comprehensive descriptions
- Code should be reviewed by at least one other agent or developer
- Tests should be updated to reflect changes

### 2. Testing Requirements
- Unit tests should cover at least 80% of new code
- Integration tests should verify API connectivity
- UI tests should ensure dashboard functionality
- Performance tests should validate response times

### 3. Deployment Process
- Changes should be deployed to staging first
- Automated smoke tests should run after deployment
- Monitoring should be in place for error detection
- Rollback procedures should be documented

## Monitoring and Alerting

### 1. System Health
- API uptime should be monitored
- Dashboard load times should be tracked
- Error rates should be logged and alerted
- Resource usage should be monitored

### 2. Data Quality
- Data freshness should be verified
- Data consistency should be checked
- Missing data should trigger alerts
- Anomalies should be detected and reported

## Continuous Learning

### 1. Feedback Integration
- User feedback should be collected and analyzed
- Usage patterns should inform feature priorities
- Performance metrics should guide optimizations
- Market changes should trigger data source updates

### 2. Technology Updates
- Dependencies should be regularly updated
- New libraries should be evaluated for benefits
- Best practices should be continuously researched
- Security vulnerabilities should be monitored

This agent configuration ensures that the Africa-USA Trade Intelligence Platform continuously evolves to become the most sophisticated and robust system for Terrence Dupree's goal of becoming the #1 Africa-USA agriculture broker globally.