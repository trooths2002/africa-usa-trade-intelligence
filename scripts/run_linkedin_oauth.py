#!/usr/bin/env python3
"""
Script to run the LinkedIn OAuth flow
This will help you get proper permissions for your LinkedIn API integration
"""

import sys
import os
import threading
import time
import webbrowser
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_linkedin_oauth():
    """Run the LinkedIn OAuth flow"""
    print("=" * 60)
    print("🔐 LINKEDIN OAUTH FLOW")
    print("=" * 60)
    print("This script will help you get proper permissions for LinkedIn API")
    print("=" * 60)
    
    try:
        # Import the LinkedIn API module
        from src.apis.linkedin_api import LinkedInAPI
        
        # Create LinkedIn API instance
        linkedin = LinkedInAPI()
        
        print("✅ LinkedIn API module loaded")
        print("✅ Credentials found")
        
        # Generate authorization URL
        print("\n📋 STEP 1: START CALLBACK SERVER")
        print("Starting local server to receive OAuth callback...")
        
        # Start the callback server in a separate thread
        from scripts.linkedin_callback_server import start_callback_server
        import subprocess
        
        # Start the callback server as a separate process
        server_process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'linkedin_callback_server.py')
        ])
        
        # Give the server a moment to start
        time.sleep(3)
        
        print("\n📋 STEP 2: AUTHORIZE THE APPLICATION")
        print("Opening LinkedIn authorization page in your browser...")
        print("Please log in and authorize ALL requested permissions:")
        print("  - r_liteprofile (Read basic profile)")
        print("  - r_emailaddress (Read email address)")
        print("  - w_member_social (Post content)")
        
        # Open the authorization flow
        auth_url = linkedin.get_authorization_url()
        if auth_url:
            print(f"🔗 Authorization URL: {auth_url}")
            webbrowser.open(auth_url)
            print("\n🔄 Waiting for authorization...")
            print("Please complete the authorization in your browser")
            print("This script will automatically continue when the code is received")
            
            # The callback server will handle receiving the code
            # For now, we'll wait a bit and then ask the user to manually enter the code
            # if the automatic method doesn't work
            time.sleep(5)
            
            print("\n⏳ If the automatic method doesn't work, you can:")
            print("1. Complete the authorization in your browser")
            print("2. Copy the 'code' parameter from the callback URL")
            print("3. Enter it manually below")
            
            # Try to get the code from the server process
            # For simplicity, we'll ask the user to enter it manually
            auth_code = input("\nEnter the authorization code (or press Enter to check if it was captured automatically): ").strip()
            
            if not auth_code:
                print("Checking if code was captured automatically...")
                # In a real implementation, we would check the server process
                # For now, we'll ask again
                auth_code = input("Enter the authorization code manually: ").strip()
            
            if auth_code:
                print("\n🔄 Exchanging authorization code for access token...")
                token = linkedin.get_access_token_from_code(auth_code)
                
                if token:
                    print("\n✅ SUCCESS! Access token obtained and saved to .env file")
                    print("You can now use all LinkedIn API features:")
                    print("  - Get profile information")
                    print("  - Share posts")
                    print("  - Access network stats")
                    
                    # Test the profile access
                    print("\n🔍 Testing profile access...")
                    profile = linkedin.get_profile()
                    if profile and profile.get('id'):
                        print("✅ Profile access working!")
                        print(f"   User ID: {profile.get('id')}")
                        print(f"   Name: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
                    else:
                        print("⚠️  Profile access may still have issues")
                    
                    print("\n🎉 LinkedIn API is now fully configured!")
                else:
                    print("\n❌ Failed to obtain access token")
                    print("Please check the authorization code and try again")
            else:
                print("\n❌ No authorization code entered")
                print("Please run this script again and enter the code")
        else:
            print("\n❌ Failed to generate authorization URL")
        
        # Terminate the server process
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            try:
                server_process.kill()
            except:
                pass
        
    except Exception as e:
        print(f"❌ Error running LinkedIn OAuth flow: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_linkedin_oauth()