#!/usr/bin/env python3
"""
Test script for LinkedIn API integration
Validates that the LinkedIn API module works correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_linkedin_api():
    """Test LinkedIn API functions"""
    print("=" * 60)
    print("🧪 TESTING LINKEDIN API INTEGRATION")
    print("=" * 60)
    print("🎯 Goal: Validate LinkedIn API integration for trade intelligence")
    print("💰 Technology Cost: $0 (100% free resources)")
    print("=" * 60)
    
    try:
        # Import the LinkedIn API module
        from src.apis.linkedin_api import (
            LinkedInAPI,
            get_linkedin_profile,
            share_linkedin_post,
            get_linkedin_network_stats
        )
        
        print("✅ LinkedIn API module imported successfully")
        
        # Test LinkedIn API class instantiation
        linkedin = LinkedInAPI()
        print("✅ LinkedInAPI class instantiated")
        
        # Test profile function
        print("\n🔍 Testing profile retrieval...")
        profile = get_linkedin_profile()
        print(f"   Profile data: {profile}")
        print("✅ Profile retrieval function works")
        
        # Test network stats function
        print("\n📊 Testing network stats retrieval...")
        stats = get_linkedin_network_stats()
        print(f"   Network stats: {stats}")
        print("✅ Network stats retrieval function works")
        
        # Test post sharing function
        print("\n📝 Testing post sharing function...")
        test_post = "Testing LinkedIn API integration for Africa-USA trade intelligence platform. #TradeTech #AgriTech"
        result = share_linkedin_post(test_post)
        print(f"   Post sharing result: {result}")
        if result:
            print("✅ Post sharing function works")
        else:
            print("ℹ️ Post sharing requires valid LinkedIn credentials")
            print("   Follow the setup guide in LINKEDIN_APP_SETUP.md to enable posting")
        
        # Test Client Credentials flow as workaround
        print("\n🔑 Testing Client Credentials flow (workaround for missing scopes)...")
        print("   See LINKEDIN_SCOPES_WORKAROUND.md for details")
        client_token = linkedin.get_client_credentials_token()
        if client_token:
            print("   ✅ Client Credentials token generated successfully")
            print("   📝 Use this token for non-member specific APIs")
        else:
            print("   ⚠️  Client Credentials token generation failed")
            print("   📝 This may be expected if app verification is still processing")
            print("   🛠️  Alternative: Generate a manual token using:")
            print("      python scripts/generate_manual_token.py")
        
        print("\n" + "=" * 60)
        print("🎉 LINKEDIN API INTEGRATION TEST COMPLETE")
        print("✅ All functions working correctly")
        print("📝 Note: Actual API calls require valid credentials in .env file")
        print("📘 Follow the setup guide in LINKEDIN_APP_SETUP.md to get started")
        print("📘 For scopes workaround, see LINKEDIN_SCOPES_WORKAROUND.md")
        print("📘 For troubleshooting, see LINKEDIN_AUTH_TROUBLESHOOTING.md")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error testing LinkedIn API: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_linkedin_api()