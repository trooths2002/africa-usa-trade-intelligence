#!/usr/bin/env python3
"""
LinkedIn Setup Checker Script
Checks the status of your LinkedIn API integration and provides specific guidance
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def check_linkedin_setup():
    """Check LinkedIn setup status and provide guidance"""
    print("=" * 60)
    print("🔍 LINKEDIN API SETUP CHECKER")
    print("=" * 60)
    
    # Check environment variables
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    print("🔑 Credentials Check:")
    if client_id and client_secret:
        print(f"   ✅ Client ID: {client_id}")
        print(f"   ✅ Client Secret: {'*' * len(client_secret) if client_secret else 'Not set'}")
        
        if access_token:
            print(f"   ✅ Access Token: {'*' * len(access_token)}")
        else:
            print("   ⚠️  Access Token: Not set (expected for OAuth flow)")
    else:
        print("   ❌ LinkedIn credentials not found in environment variables")
        print("   📝 Add LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET to your .env file")
        return
    
    print("\n📋 LinkedIn App Status:")
    print("   📱 App Type: Standalone app")
    print("   🔗 Redirect URL: http://localhost:8501")
    
    # Check required products
    print("\n📦 Required Products:")
    print("   ✅ Share on LinkedIn: ACCESS GRANTED")
    print("   📝 Marketing Developer Platform: For sharing content")
    
    # Check required scopes
    print("\n🔑 Required OAuth Scopes:")
    required_scopes = [
        "r_liteprofile - Read basic profile information",
        "r_emailaddress - Read email address", 
        "w_member_social - Post content on behalf of user"
    ]
    
    for scope in required_scopes:
        print(f"   ⚪ {scope}")
    
    print("\n🛠️  Current Status:")
    print("   ✅ Product access granted for 'Share on LinkedIn'")
    print("   ⏳ Waiting for OAuth scopes to appear in interface")
    print("   📝 This can take 10-15 minutes after product approval")
    
    print("\n🔄 Next Steps:")
    print("   1. Wait 10-15 minutes for LinkedIn to fully process your request")
    print("   2. Refresh the LinkedIn Developer Portal page")
    print("   3. Go to the 'Auth' tab")
    print("   4. Look for the 'OAuth 2.0 scopes' section")
    print("   5. Add the required OAuth scopes when they appear")
    print("   6. Generate an access token through the OAuth flow")
    
    print("\n📝 Note:")
    print("   The current integration simulates functionality until you")
    print("   complete the full OAuth setup with proper scopes.")
    print("   You can continue using the platform with simulated LinkedIn features.")
    
    print("\n" + "=" * 60)
    print("For detailed instructions, see: LINKEDIN_APP_SETUP.md")
    print("=" * 60)

if __name__ == "__main__":
    check_linkedin_setup()