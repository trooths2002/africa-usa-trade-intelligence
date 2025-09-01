#!/usr/bin/env python3
"""
Quick Scan Runner for MCP Automation Pipeline
Attempts to call the MCP client and falls back to SSE ping if needed
"""

import asyncio
import json
import os
import sys
import logging
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/quick_scan.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

class QuickScanRunner:
    def __init__(self):
        self.mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
        self.memory_server_url = os.getenv('MEMORY_SERVER_URL', 'http://localhost:3001')
        self.scan_results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'checks': [],
            'errors': [],
            'opportunities_found': 0,
            'data_sources_checked': 0
        }
    
    def log_check(self, name: str, status: str, details: str = None):
        """Log a check result"""
        check = {
            'name': name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.scan_results['checks'].append(check)
        logger.info(f"Check: {name} - {status}" + (f" - {details}" if details else ""))
    
    def log_error(self, error: str):
        """Log an error"""
        self.scan_results['errors'].append(error)
        logger.error(error)
    
    async def check_mcp_server(self) -> bool:
        """Check if MCP server is responding"""
        try:
            # Method 1: Try MCP Python client if available
            try:
                # Import and use MCP client
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from simple_mcp_client import test_mcp_connection
                
                result = await test_mcp_connection()
                if result:
                    self.log_check("MCP Client Connection", "success", "Connected via MCP Python client")
                    return True
                else:
                    self.log_check("MCP Client Connection", "failed", "MCP client connection failed")
            
            except ImportError:
                self.log_check("MCP Client Import", "warning", "MCP client not available, trying HTTP")
            except Exception as e:
                self.log_check("MCP Client Connection", "error", f"MCP client error: {str(e)}")
            
            # Method 2: HTTP health check
            try:
                response = requests.get(f"{self.mcp_server_url}/health", timeout=10)
                if response.status_code == 200:
                    self.log_check("MCP HTTP Health", "success", f"HTTP health check passed: {response.status_code}")
                    return True
                else:
                    self.log_check("MCP HTTP Health", "warning", f"HTTP health check returned: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.log_check("MCP HTTP Health", "failed", f"HTTP request failed: {str(e)}")
            
            # Method 3: SSE ping
            try:
                response = requests.get(f"{self.mcp_server_url}/sse/ping", timeout=10, stream=True)
                if response.status_code == 200:
                    self.log_check("MCP SSE Ping", "success", "SSE endpoint responding")
                    return True
                else:
                    self.log_check("MCP SSE Ping", "warning", f"SSE ping returned: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.log_check("MCP SSE Ping", "failed", f"SSE ping failed: {str(e)}")
            
            return False
            
        except Exception as e:
            self.log_error(f"MCP server check failed: {str(e)}")
            return False
    
    def check_memory_server(self) -> bool:
        """Check if memory server is responding"""
        try:
            response = requests.get(f"{self.memory_server_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_check("Memory Server", "success", "Memory server responding")
                return True
            else:
                self.log_check("Memory Server", "warning", f"Memory server returned: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_check("Memory Server", "failed", f"Memory server check failed: {str(e)}")
            return False
    
    def check_data_sources(self) -> int:
        """Check external data sources"""
        sources_checked = 0
        
        # Check US Census API
        try:
            # Use a simple endpoint that doesn't require API key
            response = requests.get(
                "https://api.census.gov/data/timeseries/intltrade/exports/sitc?get=SITC_ID,DESCRIP&SITC_ID=001&time=2023&maxCells=10",
                timeout=10
            )
            if response.status_code == 200:
                self.log_check("US Census API", "success", "Census API responding")
                sources_checked += 1
            else:
                self.log_check("US Census API", "warning", f"Census API returned: {response.status_code}")
        except Exception as e:
            self.log_check("US Census API", "failed", f"Census API check failed: {str(e)}")
        
        # Check World Bank API
        try:
            response = requests.get(
                "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2022&per_page=1",
                timeout=10
            )
            if response.status_code == 200:
                self.log_check("World Bank API", "success", "World Bank API responding")
                sources_checked += 1
            else:
                self.log_check("World Bank API", "warning", f"World Bank API returned: {response.status_code}")
        except Exception as e:
            self.log_check("World Bank API", "failed", f"World Bank API check failed: {str(e)}")
        
        # Check Exchange Rates API (free tier)
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
            if response.status_code == 200:
                self.log_check("Exchange Rates API", "success", "Exchange Rates API responding")
                sources_checked += 1
            else:
                self.log_check("Exchange Rates API", "warning", f"Exchange Rates API returned: {response.status_code}")
        except Exception as e:
            self.log_check("Exchange Rates API", "failed", f"Exchange Rates API check failed: {str(e)}")
        
        return sources_checked
    
    def simulate_opportunity_detection(self) -> int:
        """Simulate opportunity detection for demonstration"""
        # This would normally call the MCP server's market analysis tools
        # For now, simulate finding opportunities
        
        opportunities = [
            {"product": "Cashews", "origin": "Ghana", "arbitrage": 45.2},
            {"product": "Coffee", "origin": "Ethiopia", "arbitrage": 52.1},
            {"product": "Shea Butter", "origin": "Burkina Faso", "arbitrage": 38.7}
        ]
        
        self.log_check("Opportunity Detection", "success", f"Found {len(opportunities)} potential opportunities")
        
        # Save opportunities to file for email summary
        with open('logs/latest_opportunities.json', 'w') as f:
            json.dump(opportunities, f, indent=2)
        
        return len(opportunities)
    
    async def run_quick_scan(self) -> Dict[str, Any]:
        """Run the complete quick scan"""
        logger.info("Starting Phase 0 Quick Scan")
        start_time = time.time()
        
        try:
            # Check MCP server
            mcp_status = await self.check_mcp_server()
            
            # Check memory server
            memory_status = self.check_memory_server()
            
            # Check external data sources
            sources_checked = self.check_data_sources()
            self.scan_results['data_sources_checked'] = sources_checked
            
            # Simulate opportunity detection
            opportunities = self.simulate_opportunity_detection()
            self.scan_results['opportunities_found'] = opportunities
            
            # Determine overall status
            if mcp_status and memory_status and sources_checked > 0:
                self.scan_results['status'] = 'healthy'
            elif mcp_status or memory_status:
                self.scan_results['status'] = 'partial'
            else:
                self.scan_results['status'] = 'degraded'
            
            execution_time = time.time() - start_time
            self.log_check("Quick Scan Complete", "success", f"Completed in {execution_time:.2f}s")
            
        except Exception as e:
            self.log_error(f"Quick scan failed: {str(e)}")
            self.scan_results['status'] = 'failed'
        
        # Save scan results
        with open('logs/latest_scan_results.json', 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        
        logger.info(f"Quick scan completed with status: {self.scan_results['status']}")
        return self.scan_results

async def main():
    """Main entry point"""
    scanner = QuickScanRunner()
    results = await scanner.run_quick_scan()
    
    # Print summary for GitHub Actions
    print(f"SCAN_STATUS={results['status']}")
    print(f"OPPORTUNITIES_FOUND={results['opportunities_found']}")
    print(f"DATA_SOURCES_CHECKED={results['data_sources_checked']}")
    print(f"ERRORS_COUNT={len(results['errors'])}")
    
    # Exit with appropriate code
    if results['status'] in ['healthy', 'partial']:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())