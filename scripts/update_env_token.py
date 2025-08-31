#!/usr/bin/env python3
"""
Script to help update the LinkedIn access token in the .env file
"""

import os

def update_env_token():
    """Help update the LinkedIn access token in the .env file"""
    env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    print("=" * 60)
    print("🔐 UPDATE LINKEDIN ACCESS TOKEN IN .ENV FILE")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists(env_file_path):
        print("❌ .env file not found!")
        return
    
    # Read current .env file
    with open(env_file_path, 'r') as f:
        lines = f.readlines()
    
    # Display current LinkedIn settings
    print("Current LinkedIn settings in .env file:")
    for line in lines:
        if 'LINKEDIN_' in line and not line.strip().startswith('#'):
            print(f"  {line.strip()}")
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS:")
    print("1. Generate a token using the LinkedIn Developer Portal:")
    print("   - Go to https://www.linkedin.com/developers/")
    print("   - Select your app")
    print("   - Go to the 'Auth' tab")
    print("   - Scroll to 'OAuth 2.0 tools' section")
    print("   - Click 'Token Generator'")
    print("   - Select scopes and generate token")
    print("2. Copy the generated token")
    print("3. Update your .env file manually with the token:")
    print("   LINKEDIN_ACCESS_TOKEN=your_actual_token_here")
    
    print("\n📝 NOTE: This script doesn't automatically update the file")
    print("   for security reasons. You need to manually edit the .env file.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    update_env_token()