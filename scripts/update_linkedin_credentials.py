#!/usr/bin/env python3
"""
Script to help update LinkedIn API credentials in the .env file
"""

import os

def update_linkedin_credentials():
    """Help update LinkedIn API credentials in the .env file"""
    env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    print("=" * 60)
    print("🔐 LINKEDIN API CREDENTIALS UPDATE")
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
    print("📋 STEP 1: UPDATE YOUR CLIENT SECRET")
    print("1. Go to https://www.linkedin.com/developers/")
    print("2. Log in to your LinkedIn Developer account")
    print("3. Select your app: 'Free World Trade Africa-USA Trade Intelligence'")
    print("4. Navigate to the 'Auth' tab")
    print("5. Copy your actual Client Secret (click the eye icon to reveal it)")
    print("")
    
    update_secret = input("Do you want to update the Client Secret? (y/n): ")
    
    if update_secret.lower() == 'y':
        new_secret = input("Enter your LinkedIn Client Secret: ")
        
        if new_secret:
            # Update the LINKEDIN_CLIENT_SECRET line
            updated_lines = []
            for line in lines:
                if line.startswith('LINKEDIN_CLIENT_SECRET='):
                    updated_lines.append(f'LINKEDIN_CLIENT_SECRET={new_secret}\n')
                else:
                    updated_lines.append(line)
            
            # Write back to the .env file
            with open(env_file_path, 'w') as f:
                f.writelines(updated_lines)
            
            print("✅ LinkedIn Client Secret updated successfully!")
        else:
            print("❌ No secret entered. Update cancelled.")
    
    print("\n" + "=" * 60)
    print("📋 STEP 2: GENERATE ACCESS TOKEN")
    print("1. In your LinkedIn app dashboard, go to the 'Auth' tab")
    print("2. Scroll down to the 'OAuth 2.0 tools' section")
    print("3. Click on 'Token Generator'")
    print("4. Select the 'w_member_social' scope")
    print("5. Click 'Generate token'")
    print("6. Copy the generated access token")
    print("")
    
    update_token = input("Do you want to update the Access Token? (y/n): ")
    
    if update_token.lower() == 'y':
        new_token = input("Enter your LinkedIn Access Token: ")
        
        if new_token:
            # Update the LINKEDIN_ACCESS_TOKEN line
            updated_lines = []
            for line in lines:
                if line.startswith('LINKEDIN_ACCESS_TOKEN='):
                    updated_lines.append(f'LINKEDIN_ACCESS_TOKEN={new_token}\n')
                else:
                    updated_lines.append(line)
            
            # Write back to the .env file
            with open(env_file_path, 'w') as f:
                f.writelines(updated_lines)
            
            print("✅ LinkedIn Access Token updated successfully!")
        else:
            print("❌ No token entered. Update cancelled.")
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURATION COMPLETE")
    print("You can now test the LinkedIn API integration by running:")
    print("python scripts/test_linkedin_api.py")
    print("=" * 60)

if __name__ == "__main__":
    update_linkedin_credentials()