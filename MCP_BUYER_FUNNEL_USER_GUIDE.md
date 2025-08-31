# MCP BUYER FUNNEL TOOL - USER GUIDE

## Overview
The Buyer Funnel MCP Tool is a specialized component of the Africa-USA Trade Intelligence platform designed to help Free World Trade Inc. secure USA buyers across all tiers - from enterprise corporations to individual consumers.

## Key Features

### 1. Buyer Tier Identification
Automatically categorizes potential buyers into four distinct tiers based on company characteristics:
- **Enterprise Buyers**: $100M+ annual revenue, complex decision processes
- **Mid-Market Buyers**: $10M-$100M annual revenue, moderate decision processes  
- **Small Business Buyers**: $1M-$10M annual revenue, simple decision processes
- **Individual Buyers**: <$1M annual revenue, immediate decision making

### 2. Personalized Outreach Generation
Creates customized content for each buyer tier:
- LinkedIn posts tailored to the buyer's industry and size
- Email templates with personalized messaging
- Follow-up sequences optimized for each tier's engagement patterns

### 3. Engagement Tracking & Analytics
Monitors and analyzes buyer interactions:
- Connection acceptance rates
- Email open rates
- Meeting scheduling success
- Performance benchmarking against tier-specific targets

### 4. Automated Follow-up Sequences
Schedules and manages multi-step engagement plans:
- Tier-specific timing intervals
- Channel-optimized touchpoints
- Status tracking and progress monitoring

## How to Use the Buyer Funnel Tool

### Method 1: Direct Function Calls
```python
from buyer_funnel_tool import (
    identify_buyer_tier,
    generate_personalized_outreach,
    track_engagement_metrics,
    schedule_follow_up_sequence
)

# Identify buyer tier
tier = identify_buyer_tier("$50M", "Moderate", "$500K")

# Generate personalized outreach
outreach = generate_personalized_outreach(tier, "Company Name", "Industry")

# Track engagement metrics
analysis = track_engagement_metrics(tier, metrics_dict)

# Schedule follow-up sequence
actions = schedule_follow_up_sequence(tier, "Prospect Name", "2025-09-01")
```

### Method 2: Through MCP Server
The tool is integrated into the main MCP server and can be accessed through the `create_buyer_funnel` tool with these actions:
- `identify_tier`: Determine buyer tier based on company characteristics
- `generate_outreach`: Create personalized content for a specific tier
- `track_metrics`: Analyze engagement performance for a tier
- `schedule_follow_up`: Plan follow-up actions for a prospect

## Buyer Tier Characteristics

### Enterprise Buyers ($100M+ revenue)
- **Examples**: Unilever, Nestle, Kraft Heinz
- **Engagement Approach**: Executive-level introductions
- **Channels**: LinkedIn Executive Outreach, Industry Conferences
- **Success Metrics**: >50% connection rate, >20% meeting scheduled

### Mid-Market Buyers ($10M-$100M revenue)
- **Examples**: Whole Foods Market, Sprouts Farmers Market
- **Engagement Approach**: Department head outreach
- **Channels**: LinkedIn Professional Outreach, Email Campaigns
- **Success Metrics**: >70% connection rate, >40% email open rate

### Small Business Buyers ($1M-$10M revenue)
- **Examples**: Local Coffee Roasters, Specialty Food Distributors
- **Engagement Approach**: Direct owner/manager contact
- **Channels**: Social Media Marketing, Local Business Networks
- **Success Metrics**: >5% engagement rate, >10% inquiry rate

### Individual Buyers (<$1M revenue)
- **Examples**: Online Resellers, Restaurant Owners
- **Engagement Approach**: Social media and online platforms
- **Channels**: E-commerce Platforms, Social Media Ads
- **Success Metrics**: >2% click-through rate, >3% conversion rate

## Implementation Workflow

1. **Prospect Identification**: Gather basic information about potential buyers
2. **Tier Classification**: Use `identify_buyer_tier()` to categorize the prospect
3. **Content Creation**: Generate personalized outreach materials with `generate_personalized_outreach()`
4. **Initial Contact**: Deploy the outreach content through appropriate channels
5. **Performance Monitoring**: Track engagement with `track_engagement_metrics()`
6. **Follow-up Execution**: Schedule and execute follow-up actions with `schedule_follow_up_sequence()`
7. **Continuous Optimization**: Refine approach based on performance data

## Best Practices

1. **Data Quality**: Ensure accurate company revenue and industry information for proper tier classification
2. **Personalization**: Always customize outreach content with specific company details
3. **Timing**: Follow the recommended timing intervals for each tier's follow-up sequence
4. **Metrics Tracking**: Regularly monitor engagement metrics to identify optimization opportunities
5. **Compliance**: Adhere to all applicable communication regulations and platform guidelines

## Technical Requirements

- Python 3.8+
- JSON library for data handling
- Standard datetime library for scheduling
- Access to buyer_funnel.json data file

## Support
For questions about the Buyer Funnel Tool, contact:
Terrence Dupree - Africa Coverage Specialist
Free World Trade Inc.