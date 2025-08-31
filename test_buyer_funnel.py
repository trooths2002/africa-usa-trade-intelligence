#!/usr/bin/env python3
"""
Test script for the buyer funnel tool
"""

import json
import sys
import os

# Add the MCP server directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'mcp_servers', 'market_intelligence'))

from buyer_funnel_tool import (
    identify_buyer_tier,
    generate_personalized_outreach,
    track_engagement_metrics,
    schedule_follow_up_sequence
)

def test_identify_buyer_tier():
    """Test buyer tier identification"""
    print("Testing buyer tier identification...")
    
    # Test enterprise tier
    tier = identify_buyer_tier("$100M+", "Complex", "$1M+")
    print(f"Enterprise test: {tier}")
    assert tier == "enterprise"
    
    # Test mid-market tier
    tier = identify_buyer_tier("$10M-50M", "Moderate", "$100K-500K")
    print(f"Mid-market test: {tier}")
    assert tier == "mid_market"
    
    # Test small business tier
    tier = identify_buyer_tier("$1M-5M", "Simple", "$10K-100K")
    print(f"Small business test: {tier}")
    assert tier == "small_business"
    
    # Test individual tier
    tier = identify_buyer_tier("<$1M", "Simple", "<$10K")
    print(f"Individual test: {tier}")
    assert tier == "individual"
    
    print("✅ Buyer tier identification tests passed!")

def test_generate_personalized_outreach():
    """Test personalized outreach generation"""
    print("\nTesting personalized outreach generation...")
    
    # Test with mid-market tier
    outreach = generate_personalized_outreach("mid_market", "Whole Foods Market", "Retail")
    print(f"Generated outreach for mid-market: {json.dumps(outreach, indent=2)}")
    
    # Check that we got the expected fields
    assert "tier" in outreach
    assert "company_name" in outreach
    assert "industry" in outreach
    assert "linkedin_post" in outreach
    assert "email_template" in outreach
    
    print("✅ Personalized outreach generation test passed!")

def test_track_engagement_metrics():
    """Test engagement metrics tracking"""
    print("\nTesting engagement metrics tracking...")
    
    # Test with sample metrics
    metrics = {
        "connections_sent": 25,
        "connections_accepted": 15,
        "emails_sent": 30,
        "emails_opened": 18
    }
    
    analysis = track_engagement_metrics("mid_market", metrics)
    print(f"Engagement analysis: {json.dumps(analysis, indent=2)}")
    
    # Check that we got the expected fields
    assert "tier" in analysis
    assert "actual_metrics" in analysis
    assert "target_metrics" in analysis
    assert "performance_status" in analysis
    assert "recommendations" in analysis
    
    print("✅ Engagement metrics tracking test passed!")

def test_schedule_follow_up_sequence():
    """Test follow-up sequence scheduling"""
    print("\nTesting follow-up sequence scheduling...")
    
    # Test scheduling follow-ups
    actions = schedule_follow_up_sequence("enterprise", "Unilever Procurement Team", "2025-09-01")
    print(f"Scheduled follow-up actions: {json.dumps(actions, indent=2)}")
    
    # Check that we got a list of actions
    assert isinstance(actions, list)
    if actions:  # If there are actions
        assert "sequence_step" in actions[0]
        assert "action" in actions[0]
        assert "scheduled_date" in actions[0]
        assert "prospect_name" in actions[0]
        assert "status" in actions[0]
    
    print("✅ Follow-up sequence scheduling test passed!")

def main():
    """Run all tests"""
    print("🧪 Testing Buyer Funnel Tool")
    print("=" * 50)
    
    try:
        test_identify_buyer_tier()
        test_generate_personalized_outreach()
        test_track_engagement_metrics()
        test_schedule_follow_up_sequence()
        
        print("\n🎉 All tests passed! Buyer funnel tool is working correctly.")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())