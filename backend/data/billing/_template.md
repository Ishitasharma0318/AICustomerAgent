---
category: billing
subcategory: pricing | optimization | examples | free_tier
service: lambda | api-gateway | cloudwatch | data-transfer
difficulty: beginner | intermediate | advanced
last_updated: 2024-11-02
source: https://aws.amazon.com/lambda/pricing/
---

# [Pricing Topic or Cost Optimization Strategy]

## Overview
Brief overview of the pricing component or cost optimization strategy covered in this document.

## Current Pricing (as of November 2024)

### Lambda Pricing
| Component | Price | Unit |
|-----------|-------|------|
| Requests | $0.20 | per 1 million requests |
| Duration (x86) | $0.0000166667 | per GB-second |
| Duration (ARM/Graviton) | $0.0000133334 | per GB-second |
| Ephemeral storage (over 512MB) | $0.0000000309 | per GB-second |

### API Gateway Pricing
| API Type | Price | Unit |
|----------|-------|------|
| REST API | $3.50 | per million requests |
| HTTP API | $1.00 | per million requests |
| WebSocket API | $1.00 | per million messages |

### Free Tier (if applicable)
- **Lambda**: 1 million free requests per month, 400,000 GB-seconds of compute time per month
- **API Gateway**: 1 million HTTP API calls per month (12 months free)

## Cost Calculation Examples

### Example 1: Low-Traffic Application
**Scenario**: Small API with minimal traffic

**Monthly Usage**:
- 100,000 Lambda invocations
- Average duration: 200ms
- Memory: 512 MB (0.5 GB)
- API Gateway: 100,000 HTTP API calls

**Cost Breakdown**:
```
Lambda Requests: 100,000 / 1,000,000 * $0.20 = $0.02
Lambda Duration: (100,000 * 0.2s * 0.5GB) * $0.0000166667 = $0.17
API Gateway: 100,000 / 1,000,000 * $1.00 = $0.10

Total: $0.29/month (likely covered by free tier!)
```

### Example 2: High-Traffic Application
**Scenario**: Production API with significant traffic

**Monthly Usage**:
- 10 million Lambda invocations
- Average duration: 500ms
- Memory: 1024 MB (1 GB)
- API Gateway: 10 million HTTP API calls

**Cost Breakdown**:
```
Lambda Requests: 10,000,000 / 1,000,000 * $0.20 = $2.00
Lambda Duration: (10,000,000 * 0.5s * 1GB) * $0.0000166667 = $83.33
API Gateway: 10,000,000 / 1,000,000 * $1.00 = $10.00

Total: $95.33/month
```

## Cost Optimization Strategies

### Strategy 1: [Optimization Technique]
Describe the optimization strategy.

**Potential Savings**: X% reduction in costs

**How to Implement**:
1. Step 1
2. Step 2
3. Step 3

**Trade-offs**: Any performance or complexity trade-offs

### Strategy 2: [Another Technique]
Another optimization approach.

## Regional Pricing Differences
Note any significant regional pricing variations:
- US East (N. Virginia): Standard pricing
- Other regions: May vary by +/- X%

## Hidden Costs to Consider
Costs that are often overlooked:
1. **CloudWatch Logs**: $0.50 per GB ingested
2. **Data Transfer**: $0.09 per GB after first 1GB
3. **NAT Gateway** (if using VPC): $0.045 per hour + $0.045 per GB
4. **Provisioned Concurrency**: $0.0000041667 per GB-second

## Cost Comparison

### Scenario: REST API vs HTTP API
When to choose each based on cost and features:

| Feature | REST API | HTTP API |
|---------|----------|----------|
| Cost per million requests | $3.50 | $1.00 |
| Lambda authorizer | ✅ | ✅ |
| Resource policies | ✅ | ❌ |
| When to use | Need advanced features | Cost-sensitive, simple APIs |

## Free Tier Details
Detailed breakdown of what's included in the free tier:

### Always Free
- Lambda: 1M requests + 400K GB-seconds per month, forever
- API Gateway: None (always free tier ended)

### 12 Months Free
- API Gateway HTTP API: 1M calls per month for first 12 months

## Real-World Cost Examples

### Example 1: [Use Case]
Description of a real-world scenario with actual costs.

### Example 2: [Use Case]
Another practical example.

## Cost Monitoring Tips
How to monitor and track costs:
1. Set up AWS Budgets
2. Create CloudWatch billing alarms
3. Use Cost Explorer to analyze trends
4. Tag resources for cost allocation

## Frequently Asked Questions

**Q: Do I pay for failed invocations?**
A: Yes, you pay for request costs and compute time used, even if the function errors.

**Q: How are concurrent executions billed?**
A: You pay for the actual execution time and requests, not for idle concurrency.

**Q: Does caching reduce costs?**
A: API Gateway caching reduces Lambda invocations but adds caching costs ($0.02/hour for 0.5GB cache).

## Additional Resources
- AWS Pricing Calculator: https://calculator.aws/
- Cost Optimization Whitepaper
- AWS Cost Explorer documentation

