#!/usr/bin/env python3
"""
Demonstration script for using the buyer funnel tool with the MCP server

This script shows how to:
1. Identify buyer tiers
2. Generate personalized outreach
3. Track engagement metrics
4. Schedule follow-up sequences
"""

import sys
import os
import json

# Add the MCP server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'mcp_servers', 'market_intelligence'))

from buyer_funnel_tool import (
    identify_buyer_tier,
    generate_personalized_outreach,
    track_engagement_metrics,
    schedule_follow_up_sequence
)

def demonstrate_buyer_funnel():
    """Demonstrate the complete buyer funnel workflow"""
    print("🎯 MCP BUYER FUNNEL DEMONSTRATION")
    print("=" * 50)
    
    # Step 1: Identify a potential buyer's tier
    print("\n📋 STEP 1: IDENTIFY BUYER TIER")
    print("Identifying the appropriate tier for a potential buyer...")
    
    company_revenue = "$50M"
    decision_process = "Moderate"
    deal_size = "$500K"
    
    tier = identify_buyer_tier(company_revenue, decision_process, deal_size)
    print(f"Company revenue: {company_revenue}")
    print(f"Decision process: {decision_process}")
    print(f"Deal size: {deal_size}")
    print(f"✅ Identified buyer tier: {tier.upper()}")
    
    # Step 2: Generate personalized outreach
    print("\n📧 STEP 2: GENERATE PERSONALIZED OUTREACH")
    print("Creating personalized content for the buyer...")
    
    company_name = "Whole Foods Market"
    industry = "Retail"
    
    outreach = generate_personalized_outreach(tier, company_name, industry)
    print(f"Company: {company_name}")
    print(f"Industry: {industry}")
    print(f"✅ Generated personalized outreach for {tier} tier")
    print(f"LinkedIn post preview: {outreach['linkedin_post'][:100]}...")
    print(f"Email template preview: {outreach['email_template'][:100]}...")
    
    # Step 3: Track engagement metrics
    print("\n📊 STEP 3: TRACK ENGAGEMENT METRICS")
    print("Monitoring the buyer's engagement with our outreach...")
    
    metrics = {
        "connections_sent": 10,
        "connections_accepted": 7,
        "emails_sent": 5,
        "emails_opened": 4,
        "meetings_scheduled": 1
    }
    
    analysis = track_engagement_metrics(tier, metrics)
    print(f"Actual metrics: {metrics}")
    print(f"Performance status: {analysis['performance_status']}")
    print("Recommendations:")
    for rec in analysis['recommendations']:
        print(f"  • {rec}")
    
    # Step 4: Schedule follow-up sequence
    print("\n📅 STEP 4: SCHEDULE FOLLOW-UP SEQUENCE")
    print("Creating a follow-up plan for continued engagement...")
    
    prospect_name = "Whole Foods Market Procurement Team"
    initial_contact_date = "2025-09-01"
    
    actions = schedule_follow_up_sequence(tier, prospect_name, initial_contact_date)
    print(f"Prospect: {prospect_name}")
    print(f"Initial contact date: {initial_contact_date}")
    print(f"✅ Scheduled {len(actions)} follow-up actions")
    
    print("\nFollow-up schedule:")
    for action in actions[:3]:  # Show first 3 actions
        print(f"  Week {action['sequence_step']}: {action['action']} on {action['scheduled_date']}")
    
    if len(actions) > 3:
        print(f"  ... and {len(actions) - 3} more actions")
    
    print("\n" + "=" * 50)
    print("🎉 BUYER FUNNEL WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    # Summary
    print("\n📈 EXECUTIVE SUMMARY:")
    print(f"  • Target buyer: {company_name} ({tier.title()} tier)")
    print(f"  • Industry: {industry}")
    print(f"  • Personalized outreach created: LinkedIn post + Email template")
    print(f"  • Engagement tracking: {analysis['performance_status']}")
    print(f"  • Follow-up actions scheduled: {len(actions)} steps")
    print(f"  • Next action: {actions[0]['action']} on {actions[0]['scheduled_date']}")

def main():
    """Main function"""
    try:
        demonstrate_buyer_funnel()
        print("\n🚀 Ready to implement buyer funnel strategy!")
        return 0
    except Exception as e:
        print(f"\n❌ Error in demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())