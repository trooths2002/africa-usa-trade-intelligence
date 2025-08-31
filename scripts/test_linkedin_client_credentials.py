#!/usr/bin/env python3
"""
Test script for LinkedIn Client Credentials Flow (2-legged OAuth)
Tests the ability to access non-member specific APIs using client credentials
"""

import sys
import os
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

def test_client_credentials_flow():
    """Test LinkedIn Client Credentials flow"""
    print("=" * 60)
    print("🧪 TESTING LINKEDIN CLIENT CREDENTIALS FLOW (2-LEGGED OAUTH)")
    print("=" * 60)
    print("🎯 Goal: Access LinkedIn APIs that are not member specific")
    print("💰 Technology Cost: $0 (100% free resources)")
    print("=" * 60)
    
    try:
        # Import the LinkedIn API module
        from src.apis.linkedin_api import LinkedInAPI
        
        print("✅ LinkedIn API module imported successfully")
        
        # Test LinkedIn API class instantiation
        linkedin = LinkedInAPI()
        print("✅ LinkedInAPI class instantiated")
        
        # Display credentials info
        print(f"\n🔑 Credentials Info:")
        print(f"   Client ID: {linkedin.client_id}")
        print(f"   Client Secret Length: {len(linkedin.client_secret) if linkedin.client_secret else 0}")
        
        # Test client credentials token generation
        print("\n🔑 Testing client credentials token generation...")
        token = linkedin.get_client_credentials_token()
        if token:
            print(f"   ✅ Token generated: {'*' * min(20, len(token))}...")
            print("   ✅ Client Credentials flow working correctly")
            
            # Test a simple API call that doesn't require member-specific permissions
            print("\n🔍 Testing API access with client credentials...")
            try:
                # Example: Access to organization data (if available)
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                # Test with a simple endpoint that might work with client credentials
                test_url = "https://api.linkedin.com/v2/organizationAcls"
                response = requests.get(test_url, headers=headers)
                
                if response.status_code == 200:
                    print("   ✅ API access test successful")
                elif response.status_code == 403:
                    print("   ℹ️  API access test returned 403 (Forbidden)")
                    print("   📝 This is expected for some endpoints without proper permissions")
                else:
                    print(f"   ⚠️  API access test returned {response.status_code}")
                    
            except Exception as e:
                print(f"   ⚠️  API test call failed: {str(e)}")
                print("   ℹ️  This may be expected if you don't have access to specific endpoints")
        else:
            print("   ❌ Failed to generate client credentials token")
            print("   📝 Troubleshooting steps:")
            print("   1. Verify your LinkedIn app is fully verified")
            print("   2. Check that your app has access to required products")
            print("   3. Ensure Client ID and Client Secret are correct")
            print("   4. Some LinkedIn APIs require specific product permissions")
            print("   5. Client Credentials flow may not be available for all API endpoints")
        
        print("\n" + "=" * 60)
        print("🎉 LINKEDIN CLIENT CREDENTIALS FLOW TEST COMPLETE")
        print("📘 For more information, see LinkedIn API documentation on 2-legged OAuth")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error testing LinkedIn Client Credentials flow: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_client_credentials_flow()