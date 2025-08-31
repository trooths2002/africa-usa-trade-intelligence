#!/usr/bin/env python3
"""
Script to verify LinkedIn API credentials
Helps troubleshoot authentication issues
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

def verify_credentials():
    """Verify LinkedIn credentials in environment variables"""
    print("=" * 60)
    print("🔍 LINKEDIN CREDENTIALS VERIFICATION")
    print("=" * 60)
    
    # Check environment variables
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    
    print("🔑 Environment Variables Check:")
    if client_id:
        print(f"   ✅ Client ID: {client_id}")
    else:
        print("   ❌ Client ID: NOT FOUND")
        
    if client_secret:
        print(f"   ✅ Client Secret: {'*' * len(client_secret)} (length: {len(client_secret)})")
    else:
        print("   ❌ Client Secret: NOT FOUND")
    
    if client_id and client_secret:
        print("\n✅ Both credentials found in environment variables")
        print("📝 Next steps:")
        print("   1. Ensure your LinkedIn app is verified")
        print("   2. Ensure your app has access to required products")
        print("   3. Run the client credentials test script")
    else:
        print("\n❌ Missing credentials in environment variables")
        print("📝 Please add your LinkedIn credentials to the .env file:")
        print("   LINKEDIN_CLIENT_ID=your_client_id")
        print("   LINKEDIN_CLIENT_SECRET=your_client_secret")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    verify_credentials()