# Billing & Pricing Agent - Data Directory

## Purpose
This directory contains documentation for the **Billing & Pricing Agent** which uses a **Hybrid RAG/CAG** strategy.

## Agent Behavior
- **Retrieval Strategy**: Hybrid RAG/CAG
- **How it works**: 
  - On first query in a session: Performs RAG to retrieve relevant pricing information
  - Caches the retrieved pricing data for the session
  - Subsequent queries in the same session use the cached context
- **Use Case**: Pricing questions, cost optimization, billing estimates, free tier information

## Data to Collect

### Categories to Include:

1. **Lambda Pricing**
   - Request pricing (per million requests)
   - Duration pricing (per GB-second)
   - Compute pricing by architecture (x86, ARM/Graviton)
   - Provisioned concurrency pricing
   - Free tier limits
   - Regional pricing differences

2. **API Gateway Pricing**
   - REST API pricing
   - HTTP API pricing
   - WebSocket API pricing
   - Caching costs
   - Data transfer costs
   - Free tier limits

3. **Related Service Costs**
   - CloudWatch Logs pricing
   - CloudWatch metrics pricing
   - X-Ray pricing
   - Data transfer costs
   - NAT Gateway costs (for VPC)

4. **Cost Optimization**
   - Right-sizing functions
   - Architecture optimization
   - Caching strategies
   - Reserved concurrency vs on-demand
   - ARM/Graviton cost savings
   - Reducing cold starts
   - API Gateway HTTP vs REST cost comparison

5. **Billing Examples**
   - Real-world cost calculations
   - Monthly cost estimates
   - Traffic pattern examples
   - Comparison scenarios

6. **Free Tier Information**
   - Lambda free tier details
   - API Gateway free tier details
   - Always free vs 12-month free
   - Free tier monitoring

## File Naming Convention
Use descriptive names with hyphens:
- `lambda-pricing-details.md`
- `api-gateway-pricing-comparison.md`
- `cost-optimization-strategies.md`
- `free-tier-limits.md`

## Metadata Template
Each file should start with:
```markdown
---
category: billing
subcategory: pricing | optimization | examples | free_tier
service: lambda | api-gateway | cloudwatch | data-transfer
difficulty: beginner | intermediate | advanced
last_updated: YYYY-MM-DD
---
```

## Target: 6-10 Documents
Focus on accurate pricing information and practical cost optimization advice.

