#!/usr/bin/env python3
"""
Simple test for buyer funnel tool
"""

import sys
import os

# Add the MCP server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'mcp_servers', 'market_intelligence'))

from buyer_funnel_tool import (
    identify_buyer_tier,
    generate_personalized_outreach,
    track_engagement_metrics,
    schedule_follow_up_sequence
)

def main():
    print("Testing buyer funnel tool...")
    
    # Test tier identification
    print("\n1. Testing tier identification:")
    enterprise_tier = identify_buyer_tier("$100M+", "Complex", "$1M+")
    print(f"Enterprise tier: {enterprise_tier}")
    
    mid_market_tier = identify_buyer_tier("$10M-50M", "Moderate", "$100K-500K")
    print(f"Mid-market tier: {mid_market_tier}")
    
    small_business_tier = identify_buyer_tier("$1M-5M", "Simple", "$10K-100K")
    print(f"Small business tier: {small_business_tier}")
    
    individual_tier = identify_buyer_tier("<$1M", "Simple", "<$10K")
    print(f"Individual tier: {individual_tier}")
    
    # Test outreach generation
    print("\n2. Testing outreach generation:")
    outreach = generate_personalized_outreach("mid_market", "Whole Foods Market", "Retail")
    print(f"Generated outreach for {outreach['tier']}: {outreach['company_name']} in {outreach['industry']}")
    
    # Test metrics tracking
    print("\n3. Testing metrics tracking:")
    metrics = {
        "connections_sent": 25,
        "connections_accepted": 15,
        "emails_sent": 30,
        "emails_opened": 18
    }
    analysis = track_engagement_metrics("mid_market", metrics)
    print(f"Performance status: {analysis['performance_status']}")
    
    # Test follow-up scheduling
    print("\n4. Testing follow-up scheduling:")
    actions = schedule_follow_up_sequence("enterprise", "Unilever Procurement Team", "2025-09-01")
    print(f"Scheduled {len(actions)} follow-up actions")
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    main()