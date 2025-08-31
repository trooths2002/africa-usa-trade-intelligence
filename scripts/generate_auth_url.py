#!/usr/bin/env python3
"""
Script to generate the LinkedIn OAuth authorization URL
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def generate_auth_url():
    """Generate the LinkedIn OAuth authorization URL"""
    print("=" * 60)
    print("🔐 LINKEDIN OAUTH AUTHORIZATION URL GENERATOR")
    print("=" * 60)
    
    try:
        # Import the LinkedIn API module
        from src.apis.linkedin_api import LinkedInAPI
        
        # Create LinkedIn API instance
        linkedin = LinkedInAPI()
        
        print("✅ LinkedIn API module loaded")
        
        # Check credentials
        if not linkedin.client_id or not linkedin.client_secret:
            print("❌ LinkedIn credentials not found")
            print("Please make sure LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET")
            print("are set in your .env file")
            return
        
        print(f"✅ Client ID: {linkedin.client_id}")
        print(f"✅ Redirect URI: {linkedin.redirect_uri}")
        
        # Generate authorization URL
        auth_url = linkedin.get_authorization_url()
        
        if auth_url:
            print("\n" + "=" * 60)
            print("📋 AUTHORIZATION URL")
            print("=" * 60)
            print("Copy and paste this URL in your browser:")
            print("")
            print(auth_url)
            print("")
            print("=" * 60)
            print("NEXT STEPS:")
            print("1. Open the URL in your browser")
            print("2. Log in to LinkedIn and authorize the application")
            print("3. After authorization, you'll be redirected to a localhost URL")
            print("4. Copy that URL from your browser's address bar")
            print("5. Run 'python scripts/exchange_code_for_token.py'")
            print("6. Paste the URL when prompted")
            print("=" * 60)
        else:
            print("❌ Failed to generate authorization URL")
            
    except Exception as e:
        print(f"❌ Error generating authorization URL: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_auth_url()