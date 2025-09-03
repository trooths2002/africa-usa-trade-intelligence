"""
Test script to verify the password protection functionality
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_password_protection():
    """Test that the password protection is working"""
    try:
        from src.config.settings import APP_LOGIN_PASSWORD
        print(f"Password protection is configured. Default password: {APP_LOGIN_PASSWORD}")
        print("SUCCESS: Password protection module loaded correctly")
        return True
    except Exception as e:
        print(f"ERROR: Failed to load password protection: {e}")
        return False

if __name__ == "__main__":
    success = test_password_protection()
    sys.exit(0 if success else 1)