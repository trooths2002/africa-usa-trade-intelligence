#!/usr/bin/env python3
"""
Simple script to help get LinkedIn access token
This approach doesn't require a localhost server
"""

import sys
import os
import webbrowser
import urllib.parse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def get_linkedin_token_simple():
    """Simple approach to get LinkedIn access token"""
    print("=" * 60)
    print("🔐 SIMPLE LINKEDIN ACCESS TOKEN GENERATOR")
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
        
        # Generate authorization URL with only available scopes
        print("\n⚠️  NOTE: Using limited scopes due to app permissions")
        print("   Available scope: w_member_social (post content)")
        print("   Missing scopes: r_liteprofile, r_emailaddress")
        
        auth_url = linkedin.get_authorization_url(scopes=["w_member_social"])
        
        if auth_url:
            print("\n" + "=" * 60)
            print("📋 STEP 1: AUTHORIZE THE APPLICATION")
            print("=" * 60)
            print("Click the link below to authorize the application:")
            print("")
            print(auth_url)
            print("")
            
            # Try to open in browser
            try:
                webbrowser.open(auth_url)
                print("✅ Browser opened automatically")
            except:
                print("⚠️  Could not open browser automatically")
                print("📋 Please copy and paste the URL above into your browser")
            
            print("\n" + "=" * 60)
            print("📋 STEP 2: GET AUTHORIZATION CODE MANUALLY")
            print("=" * 60)
            print("After authorizing in your browser:")
            print("1. You will see a 'Page not found' or similar error")
            print("2. This is NORMAL - don't worry about it")
            print("3. Look at the URL in your browser's address bar")
            print("4. It should look like this:")
            print("   http://localhost:8501/?code=XXXXXXX&state=XXXXXXX")
            print("5. Copy the ENTIRE URL from your browser's address bar")
            print("=" * 60)
            
            # Get the callback URL from user
            print("\n📋 Please paste the full URL from your browser's address bar:")
            callback_url = input("URL: ").strip()
            
            if not callback_url:
                print("❌ No URL entered")
                return
            
            # Parse the URL to extract the authorization code
            parsed_url = urllib.parse.urlparse(callback_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            # Check for errors first
            error = query_params.get('error', [None])[0]
            if error:
                error_description = query_params.get('error_description', [''])[0]
                print(f"❌ OAuth Error: {error}")
                print(f"   Description: {error_description}")
                print("\n📝 This is likely because your app doesn't have all scopes approved yet.")
                print("   We're only requesting 'w_member_social' scope now.")
                print("   Please try again, and if it fails, you may need to wait for")
                print("   LinkedIn to fully process your app permissions (can take 24-48 hours).")
                return
            
            # Extract the authorization code
            auth_code = query_params.get('code', [None])[0]
            
            if not auth_code:
                print("❌ Could not extract authorization code from URL")
                print("The URL should contain a 'code' parameter")
                print("Example: http://localhost:8501/?code=YOUR_CODE_HERE&state=...")
                return
            
            print(f"✅ Authorization code extracted: {auth_code[:10]}...")
            
            # Exchange the authorization code for an access token
            print("\n" + "=" * 60)
            print("🔄 EXCHANGING CODE FOR ACCESS TOKEN")
            print("=" * 60)
            token = linkedin.get_access_token_from_code(auth_code)
            
            if token:
                print("\n" + "=" * 60)
                print("✅ SUCCESS! Access token obtained")
                print("=" * 60)
                print(f"Access token: {token[:20]}...")
                print("The token has been automatically saved to your .env file")
                print("\n⚠️  LIMITED FUNCTIONALITY:")
                print("   With only 'w_member_social' scope, you can:")
                print("   - Share posts on LinkedIn")
                print("   - NOT access profile information")
                print("   - NOT access email address")
                print("   - NOT access network stats")
                print("\n🎉 You can now test your LinkedIn API integration:")
                print("   python scripts/test_linkedin_api.py")
                print("=" * 60)
            else:
                print("\n❌ Failed to obtain access token")
                print("Please check the authorization code and try again")
        else:
            print("❌ Failed to generate authorization URL")
            
    except KeyboardInterrupt:
        print("\n\n👋 Process interrupted by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_linkedin_token_simple()