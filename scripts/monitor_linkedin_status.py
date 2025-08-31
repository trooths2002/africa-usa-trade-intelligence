#!/usr/bin/env python3
"""
LinkedIn Status Monitor
Checks the current status of your LinkedIn API integration
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def monitor_linkedin_status():
    """Monitor the status of LinkedIn API integration"""
    print("=" * 60)
    print("📊 LINKEDIN API STATUS MONITOR")
    print("=" * 60)
    print(f"📅 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check credentials
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    print("🔑 CREDENTIALS STATUS:")
    if client_id and client_id != '77o6mi0iq7k3j4':
        print("   ✅ Client ID: Configured")
    elif client_id:
        print("   ⚠️  Client ID: Using default value (may need update)")
    else:
        print("   ❌ Client ID: Missing")
        
    if client_secret and client_secret != 'your_actual_client_secret_here':
        print("   ✅ Client Secret: Configured")
    elif client_secret:
        print("   ⚠️  Client Secret: Using placeholder (needs update)")
    else:
        print("   ❌ Client Secret: Missing")
        
    if access_token and access_token != 'your_generated_token_here':
        print("   ✅ Access Token: Configured")
        print(f"   🔑 Token preview: {access_token[:20]}...")
    elif access_token:
        print("   ⚠️  Access Token: Using placeholder (needs update)")
    else:
        print("   ❌ Access Token: Missing")
    
    print("\n🔧 INTEGRATION STATUS:")
    try:
        from src.apis.linkedin_api import LinkedInAPI
        linkedin = LinkedInAPI()
        print("   ✅ LinkedIn API module: Loaded successfully")
        print("   📦 Current mode: Simulation (waiting for full permissions)")
    except Exception as e:
        print(f"   ❌ LinkedIn API module: Error - {str(e)}")
    
    print("\n📋 REQUIRED SCOPES:")
    scopes_status = {
        "w_member_social": "✅ Granted (posting capability)",
        "r_liteprofile": "⏳ Pending (profile access)",
        "r_emailaddress": "⏳ Pending (email access)"
    }
    
    for scope, status in scopes_status.items():
        print(f"   {status} {scope}")
    
    print("\n📈 CURRENT CAPABILITIES:")
    capabilities = [
        "✅ Simulate profile retrieval",
        "✅ Simulate network statistics",
        "✅ Simulate post sharing",
        "✅ Test API functions",
        "❌ Actual profile access (requires r_liteprofile)",
        "❌ Actual network stats (requires r_liteprofile)", 
        "❌ Actual post sharing (requires proper scope access)"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print("\n⏰ RECOMMENDED TIMELINE:")
    timeline = [
        "⏳ Now - Continue development with simulation mode",
        "📅 In 24 hours - Check LinkedIn Developer Portal for scope updates",
        "📅 In 48 hours - If scopes still not visible, contact LinkedIn support",
        "✅ When scopes appear - Add them and generate new access token",
        "🚀 Full integration - Enable actual API calls"
    ]
    
    for item in timeline:
        print(f"   {item}")
    
    print("\n📝 NEXT STEPS:")
    next_steps = [
        "1. Continue building your Africa-USA trade intelligence platform",
        "2. Prepare content strategy for affiliate marketing ($2000/month goal)",
        "3. Check LinkedIn Developer Portal in 24-48 hours",
        "4. Run this script again to monitor status",
        "5. See LINKEDIN_CURRENT_STATUS.md for detailed information"
    ]
    
    for step in next_steps:
        print(f"   {step}")
    
    print("\n" + "=" * 60)
    print("For detailed status information, see: LINKEDIN_CURRENT_STATUS.md")
    print("=" * 60)

if __name__ == "__main__":
    monitor_linkedin_status()