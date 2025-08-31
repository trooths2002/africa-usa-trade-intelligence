#!/usr/bin/env python3
"""
Script to check LinkedIn environment configuration
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

def check_linkedin_env():
    """Check LinkedIn environment configuration"""
    print("=" * 60)
    print("🔍 LINKEDIN ENVIRONMENT CONFIGURATION CHECK")
    print("=" * 60)
    
    # Check environment variables
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
    
    print("🔑 Environment Variables Check:")
    if client_id:
        print(f"   ✅ LINKEDIN_CLIENT_ID: {client_id}")
    else:
        print("   ❌ LINKEDIN_CLIENT_ID: NOT FOUND")
        
    if client_secret and client_secret != 'your_actual_client_secret_here':
        print(f"   ✅ LINKEDIN_CLIENT_SECRET: {'*' * len(client_secret)}")
    elif client_secret:
        print("   ⚠️  LINKEDIN_CLIENT_SECRET: Placeholder value found")
        print("      Please update with your actual client secret")
    else:
        print("   ❌ LINKEDIN_CLIENT_SECRET: NOT FOUND")
        
    if access_token and access_token != 'your_generated_token_here':
        print(f"   ✅ LINKEDIN_ACCESS_TOKEN: {'*' * min(20, len(access_token))}...")
    elif access_token:
        print("   ⚠️  LINKEDIN_ACCESS_TOKEN: Placeholder value found")
        print("      Please update with your actual access token")
    else:
        print("   ❌ LINKEDIN_ACCESS_TOKEN: NOT FOUND")
        
    if redirect_uri:
        print(f"   ✅ LINKEDIN_REDIRECT_URI: {redirect_uri}")
    else:
        print("   ❌ LINKEDIN_REDIRECT_URI: NOT FOUND")
    
    print("\n📋 Configuration Status:")
    if client_id and client_secret and client_secret != 'your_actual_client_secret_here':
        if access_token and access_token != 'your_generated_token_here':
            print("   ✅ LinkedIn API is ready for use")
            print("   📝 You can now test LinkedIn API integration")
        else:
            print("   ⚠️  LinkedIn credentials found but access token missing")
            print("   🛠️  Generate a manual token using:")
            print("      python scripts/generate_manual_token.py")
    else:
        print("   ❌ LinkedIn API credentials not properly configured")
        print("   📝 Please update your .env file with actual credentials")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_linkedin_env()