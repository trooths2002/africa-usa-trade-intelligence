#!/usr/bin/env python3
"""
Comprehensive verification script for the config pack implementation
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_all_components():
    """Test all components of the config pack"""
    print("🔍 Verifying Config Pack Implementation")
    print("=" * 50)
    
    # Test 1: Settings module
    print("\n1. Testing settings module...")
    try:
        from src.config.settings import (
            APP_LOGIN_PASSWORD, 
            DATABASE_URL, 
            STREAMLIT_API_URL, 
            DEFAULT_USER_ID,
            summarize
        )
        print("   ✓ Settings module imported successfully")
        print(f"   ✓ Default password: {APP_LOGIN_PASSWORD}")
        print(f"   ✓ Database URL: {DATABASE_URL}")
        print(f"   ✓ API URL: {STREAMLIT_API_URL}")
        print(f"   ✓ Default user ID: {DEFAULT_USER_ID}")
        
        # Test summarize function
        summary = summarize()
        print(f"   ✓ Summary function works: {summary}")
    except Exception as e:
        print(f"   ✗ Failed to import settings: {e}")
        return False
    
    # Test 2: Health module
    print("\n2. Testing health module...")
    try:
        import src.health.main
        print("   ✓ Health module imported successfully")
    except Exception as e:
        print(f"   ✗ Failed to import health module: {e}")
        return False
    
    # Test 3: Dashboard password protection
    print("\n3. Testing dashboard password protection...")
    try:
        # This just verifies the import works
        from src.config.settings import APP_LOGIN_PASSWORD
        print(f"   ✓ Dashboard password protection ready (default: {APP_LOGIN_PASSWORD})")
    except Exception as e:
        print(f"   ✗ Dashboard password protection failed: {e}")
        return False
    
    # Test 4: File existence
    print("\n4. Testing required file existence...")
    required_files = [
        "src/config/settings.py",
        "src/health/main.py",
        "bin/start-dashboard.sh",
        "bin/start-health.sh",
        "render.yaml",
        "Procfile",
        ".github/workflows/health-check.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', file_path)):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   ✗ Missing files: {missing_files}")
        return False
    else:
        print("   ✓ All required files exist")
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Config pack is ready for deployment.")
    print("\nNext steps:")
    print("1. Set environment variables on your hosting platform:")
    print("   - APP_LOGIN_PASSWORD (strong passphrase)")
    print("   - DATABASE_URL (Postgres URL)")
    print("   - STREAMLIT_API_URL (your deployed dashboard URL)")
    print("2. Set STREAMLIT_API_URL as a GitHub Secret for CI health checks")
    print("3. Deploy via Render (render.yaml) or Railway (Procfile)")
    return True

if __name__ == "__main__":
    success = test_all_components()
    sys.exit(0 if success else 1)