#!/usr/bin/env python3
"""
Script to exchange LinkedIn OAuth authorization code for access token
"""

import sys
import os
import urllib.parse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def exchange_code_for_token():
    """Exchange authorization code for access token"""
    print("=" * 60)
    print("🔄 LINKEDIN OAUTH CODE EXCHANGE")
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
        
        # Get the callback URL from user
        print("\n📋 Please enter the full callback URL from your browser")
        print("It should look like:")
        print("  http://localhost:8501/?code=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&state=random_state_string")
        print("")
        
        callback_url = input("Enter the callback URL: ").strip()
        
        if not callback_url:
            print("❌ No URL entered")
            return
        
        # Parse the URL to extract the authorization code
        parsed_url = urllib.parse.urlparse(callback_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Extract the authorization code
        auth_code = query_params.get('code', [None])[0]
        
        if not auth_code:
            print("❌ Could not extract authorization code from URL")
            print("Make sure you copied the full URL from your browser's address bar")
            return
        
        print(f"✅ Authorization code extracted: {auth_code[:20]}...")
        
        # Exchange the authorization code for an access token
        print("\n🔄 Exchanging authorization code for access token...")
        token = linkedin.get_access_token_from_code(auth_code)
        
        if token:
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Access token obtained")
            print("=" * 60)
            print(f"Access token: {token[:20]}...")
            print("The token has been automatically saved to your .env file")
            print("=" * 60)
            print("You can now test your LinkedIn API integration:")
            print("  python scripts/test_linkedin_api.py")
            print("=" * 60)
        else:
            print("\n❌ Failed to obtain access token")
            print("Please check the authorization code and try again")
            
    except Exception as e:
        print(f"❌ Error exchanging authorization code: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    exchange_code_for_token()