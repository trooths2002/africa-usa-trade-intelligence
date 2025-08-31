#!/usr/bin/env python3
"""
Simple LinkedIn post test script
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_simple_post():
    """Test a simple LinkedIn post"""
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ No access token found")
        return False
    
    print(f"✅ Access token found: {access_token[:20]}...")
    
    # Try a simple post with the correct format
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    
    # Try with a different approach - using the person URN format that might work
    payload = {
        "author": "urn:li:person:~",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Testing LinkedIn API integration for Africa-USA trade intelligence platform. #TradeTech #AgriTech"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    print("🔄 Sending post request...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("✅ Post shared successfully!")
        return True
    else:
        print(f"❌ Failed to share post: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Let's try to understand what the correct format should be
        # by checking if we can get any user information
        try:
            # Try the userinfo endpoint
            userinfo_url = "https://api.linkedin.com/v2/userinfo"
            userinfo_response = requests.get(userinfo_url, headers=headers)
            if userinfo_response.status_code == 200:
                userinfo = userinfo_response.json()
                print(f"✅ User info: {userinfo}")
                # Try with the actual user ID from userinfo
                user_id = userinfo.get('sub')
                if user_id:
                    print(f"🔄 Trying with actual user ID: {user_id}")
                    payload["author"] = f"urn:li:person:{user_id}"
                    retry_response = requests.post(url, headers=headers, json=payload)
                    if retry_response.status_code == 201:
                        print("✅ Post shared successfully with user ID!")
                        return True
                    else:
                        print(f"❌ Still failed with user ID: {retry_response.status_code}")
                        print(f"Response: {retry_response.text}")
            else:
                print(f"❌ Failed to get user info: {userinfo_response.status_code}")
                print(f"Response: {userinfo_response.text}")
        except Exception as e:
            print(f"❌ Error getting user info: {str(e)}")
        
        return False

if __name__ == "__main__":
    test_simple_post()