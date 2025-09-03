#!/usr/bin/env python3
"""
Deployment verification script for Africa-USA Trade Intelligence Platform
"""

import os
import sys
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config.settings import APP_LOGIN_PASSWORD, DATABASE_URL, STREAMLIT_API_URL

def verify_secrets():
    """
    Verify that all required secrets are set
    """
    print("🔍 Verifying required secrets...")
    
    secrets_to_check = [
        ("APP_LOGIN_PASSWORD", APP_LOGIN_PASSWORD),
        ("DATABASE_URL", DATABASE_URL),
        ("STREAMLIT_API_URL", STREAMLIT_API_URL)
    ]
    
    missing_secrets = []
    for name, value in secrets_to_check:
        if not value or value in ["change-me", "change-me-dev", "your-secret-key-here-generate-random-string"]:
            missing_secrets.append(name)
            print(f"❌ {name}: NOT SET (current value: {value})")
        else:
            print(f"✅ {name}: SET")
    
    return len(missing_secrets) == 0

def verify_endpoints():
    """
    Verify that all required endpoints are accessible
    """
    print("\n🔍 Verifying endpoints...")
    
    endpoints_to_check = [
        ("Dashboard", STREAMLIT_API_URL),
        ("Health API", f"{STREAMLIT_API_URL}/health")
    ]
    
    failed_endpoints = []
    for name, url in endpoints_to_check:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                print(f"✅ {name}: {url} -> HTTP {response.status_code}")
            else:
                print(f"❌ {name}: {url} -> HTTP {response.status_code}")
                failed_endpoints.append(name)
        except Exception as e:
            print(f"❌ {name}: {url} -> ERROR: {e}")
            failed_endpoints.append(name)
    
    return len(failed_endpoints) == 0

def verify_database():
    """
    Verify that the database is properly configured
    """
    print("\n🔍 Verifying database configuration...")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not set")
        return False
    
    # Check if it's a PostgreSQL database
    if DATABASE_URL.startswith("postgresql://"):
        print("✅ Database type: PostgreSQL")
        # We could add more detailed checks here if needed
    elif DATABASE_URL.startswith("sqlite:///"):
        print("✅ Database type: SQLite (development only)")
    else:
        print(f"⚠️  Database type: Unknown ({DATABASE_URL[:20]}...)")
    
    # Try to initialize the database
    try:
        from src.data.init_db import init_database
        init_database()
        print("✅ Database initialization: SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Database initialization: FAILED - {e}")
        return False

def verify_data_pipelines():
    """
    Verify that data ingestion pipelines are working
    """
    print("\n🔍 Verifying data pipelines...")
    
    try:
        # Test a simple data job
        from src.data.jobs.refresh_arbitrage import main as test_arbitrage
        test_arbitrage()
        print("✅ Arbitrage engine: WORKING")
        return True
    except Exception as e:
        print(f"❌ Arbitrage engine: FAILED - {e}")
        return False

def verify_monitoring():
    """
    Verify that monitoring is properly configured
    """
    print("\n🔍 Verifying monitoring setup...")
    
    # Check if UptimeRobot API key is set
    uptime_key = os.getenv("UPTIMEROBOT_API_KEY")
    if uptime_key:
        print("✅ UptimeRobot API key: SET")
    else:
        print("⚠️  UptimeRobot API key: NOT SET (optional for external monitoring)")
    
    # Check if monitoring agent can be imported
    try:
        from src.monitoring.agent import MonitoringAgent
        print("✅ Monitoring agent: IMPORT SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Monitoring agent: IMPORT FAILED - {e}")
        return False

def main():
    """
    Main verification function
    """
    print("🚀 Africa-USA Trade Intelligence Platform - Deployment Verification")
    print("=" * 70)
    
    # Run all verification checks
    checks = [
        ("Secrets verification", verify_secrets),
        ("Endpoint verification", verify_endpoints),
        ("Database verification", verify_database),
        ("Data pipeline verification", verify_data_pipelines),
        ("Monitoring verification", verify_monitoring)
    ]
    
    results = []
    for check_name, check_function in checks:
        print(f"\n{check_name}")
        print("-" * len(check_name))
        try:
            result = check_function()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name}: FAILED - {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All verification checks passed! The platform is ready for production use.")
        return 0
    else:
        print(f"\n⚠️  {failed} verification check(s) failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())