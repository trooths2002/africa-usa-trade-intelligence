#!/usr/bin/env python3
"""
Test script for the MCP server with buyer funnel tool
"""

import sys
import os
import json

# Add the MCP server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'mcp_servers', 'market_intelligence'))

def test_buyer_funnel_tool():
    """Test the buyer funnel tool through the MCP server interface"""
    print("Testing buyer funnel tool via MCP server interface...")
    
    # Import the functions we need
    from buyer_funnel_tool import (
        identify_buyer_tier,
        generate_personalized_outreach,
        track_engagement_metrics,
        schedule_follow_up_sequence
    )
    
    # Test 1: Identify buyer tier
    print("\n1. Testing buyer tier identification:")
    tier = identify_buyer_tier("$100M+", "Complex", "$1M+")
    print(f"Enterprise tier identified: {tier}")
    
    # Test 2: Generate personalized outreach
    print("\n2. Testing personalized outreach generation:")
    outreach = generate_personalized_outreach("mid_market", "Whole Foods Market", "Retail")
    print(f"Generated outreach for {outreach['company_name']} in {outreach['industry']}")
    print(f"Follow-up sequence has {len(outreach['follow_up_sequence'])} steps")
    
    # Test 3: Track engagement metrics
    print("\n3. Testing engagement metrics tracking:")
    metrics = {
        "connections_sent": 25,
        "connections_accepted": 15,
        "emails_sent": 30,
        "emails_opened": 18
    }
    analysis = track_engagement_metrics("mid_market", metrics)
    print(f"Performance status: {analysis['performance_status']}")
    
    # Test 4: Schedule follow-up sequence
    print("\n4. Testing follow-up sequence scheduling:")
    actions = schedule_follow_up_sequence("enterprise", "Unilever Procurement Team", "2025-09-01")
    print(f"Scheduled {len(actions)} follow-up actions")
    if actions:
        print(f"First action: {actions[0]['action']} on {actions[0]['scheduled_date']}")
    
    print("\n✅ All MCP buyer funnel tool tests passed!")

def main():
    """Run all tests"""
    print("🧪 Testing MCP Server Buyer Funnel Tool Integration")
    print("=" * 60)
    
    try:
        test_buyer_funnel_tool()
        print("\n🎉 All tests completed successfully!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())