---
category: billing
subcategory: free_tier
service: lambda
difficulty: beginner
last_updated: 2024-11-02
source: https://aws.amazon.com/free/
---

# AWS Lambda and API Gateway Free Tier

## Overview
AWS offers generous free tier limits for Lambda and API Gateway, making it easy to get started and run small applications at no cost.

## Lambda Free Tier

### Always Free (No Expiration)
The Lambda free tier **never expires** and is available to all AWS customers.

**Monthly Limits**:
- **1 million free requests** per month
- **400,000 GB-seconds** of compute time per month

### What is a GB-Second?
GB-seconds = (Memory in GB) × (Duration in seconds)

**Examples**:
- 128 MB (0.125 GB) for 10 seconds = 1.25 GB-seconds
- 512 MB (0.5 GB) for 1 second = 0.5 GB-seconds
- 1024 MB (1 GB) for 5 seconds = 5 GB-seconds

## API Gateway Free Tier

### HTTP API (Always Free)
- **1 million HTTP API calls** per month (always free)

### REST API (12 Months Free for New Customers)
- **1 million REST API calls** per month
- **Only for first 12 months** after account creation
- After 12 months: $3.50 per million requests

### WebSocket API
- **1 million messages** per month (first 12 months)

## Calculating Free Tier Usage

### Example 1: Small Website API
```
Monthly traffic:
- 50,000 API requests
- Lambda: 200ms average, 512MB memory

Lambda Calculations:
- Requests: 50,000 (well under 1M free tier) ✅
- GB-seconds: 50,000 × 0.2s × 0.5GB = 5,000 GB-seconds
- Free tier: 400,000 GB-seconds
- Usage: 1.25% of free tier ✅

API Gateway (HTTP API):
- Requests: 50,000 (under 1M free tier) ✅

TOTAL COST: $0.00 (100% covered by free tier!)
```

### Example 2: Medium Traffic Application
```
Monthly traffic:
- 2 million API requests
- Lambda: 150ms average, 256MB memory

Lambda Calculations:
- Requests: 2M total
  - Free: 1M requests
  - Paid: 1M requests × $0.20/M = $0.20
  
- GB-seconds: 2M × 0.15s × 0.25GB = 75,000 GB-seconds
  - Free: 75,000 (under 400K limit) ✅
  - Paid: $0.00

API Gateway (HTTP API):
- Requests: 2M total
  - Free: 1M requests
  - Paid: 1M × $1.00/M = $1.00

TOTAL COST: $1.20/month
```

### Example 3: Memory-Intensive Function
```
Monthly traffic:
- 500,000 API requests
- Lambda: 1 second average, 3008MB (3GB) memory

Lambda Calculations:
- Requests: 500,000 (under 1M free tier) ✅
  
- GB-seconds: 500,000 × 1s × 3GB = 1,500,000 GB-seconds
  - Free: 400,000 GB-seconds
  - Paid: 1,100,000 GB-seconds
  - Cost: 1,100,000 × $0.0000166667 = $18.33

API Gateway: Free (under 1M) ✅

TOTAL COST: $18.33/month
```

## How to Maximize Free Tier

### 1. Use Memory Efficiently
Lower memory = more invocations in free tier

```python
# If your function doesn't need much memory
# Use 128MB instead of default 1024MB
# 
# 400,000 GB-seconds at 128MB = 3.2M seconds of execution
# 400,000 GB-seconds at 1024MB = 400K seconds of execution
```

### 2. Optimize Duration
Faster execution = more invocations in free tier

```python
# ❌ Slow (1 second per invocation)
# Free tier allows: 400,000 invocations at 1GB

# ✅ Fast (0.1 seconds per invocation)  
# Free tier allows: 4,000,000 invocations at 1GB
```

### 3. Use HTTP API Instead of REST API
HTTP API has always-free tier, REST API only 12 months

### 4. Cache Responses
Reduce number of Lambda invocations

```python
# Cache frequent queries
# Each cache hit saves a Lambda invocation
```

### 5. Batch Operations
Process multiple items per invocation

```python
# ❌ 1000 invocations for 1000 items
for item in items:
    invoke_lambda(item)

# ✅ 10 invocations for 1000 items (batches of 100)
for batch in batched_items:
    invoke_lambda(batch)
```

## Free Tier Limits by Region

Free tier is **per account**, not per region. Usage across all regions counts toward your free tier limit.

**Example**:
- us-east-1: 500K requests
- eu-west-1: 600K requests
- **Total**: 1.1M requests (100K exceed free tier)

## Monitoring Free Tier Usage

### AWS Billing Dashboard
1. Go to AWS Billing Console
2. Navigate to "Free Tier"
3. See current usage and forecasts

### Set Up Alerts
```bash
# Create billing alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "FreeTierExceeded" \
  --alarm-description "Alert when free tier exceeded" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --evaluation-periods 1 \
  --threshold 1.0 \
  --comparison-operator GreaterThanThreshold
```

### CloudWatch Logs
Monitor invocations and duration:
```bash
# Get invocation count
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time 2024-11-01T00:00:00Z \
  --end-time 2024-11-30T23:59:59Z \
  --period 2592000 \
  --statistics Sum
```

## Common Misconceptions

### ❌ "Free tier is only for new accounts"
✅ **False**: Lambda free tier is always available, even for old accounts

### ❌ "Free tier resets annually"
✅ **False**: Lambda free tier resets monthly

### ❌ "I can use unlimited Lambda if I stay under 1M requests"
✅ **False**: You also need to stay under 400K GB-seconds of compute

### ❌ "Provisioned concurrency is included"
✅ **False**: Provisioned concurrency has separate charges

## Free Tier Comparison Table

| Service | Free Tier | Duration | Notes |
|---------|-----------|----------|-------|
| Lambda Requests | 1M/month | Always free | Never expires |
| Lambda Compute | 400K GB-sec/month | Always free | Never expires |
| HTTP API | 1M calls/month | Always free | Never expires |
| REST API | 1M calls/month | 12 months | New accounts only |
| WebSocket API | 1M messages/month | 12 months | New accounts only |
| CloudWatch Logs | 5 GB/month | Always free | For Lambda logs |

## Cost After Free Tier

Once you exceed free tier:

```python
# Lambda
requests_cost = (total_requests - 1_000_000) / 1_000_000 * 0.20
compute_cost = (total_gb_seconds - 400_000) * 0.0000166667

# API Gateway (HTTP API)
api_cost = (total_requests - 1_000_000) / 1_000_000 * 1.00

total_monthly_cost = requests_cost + compute_cost + api_cost
```

## Tips for Staying in Free Tier

1. **Use efficient code**: Faster = more invocations in free tier
2. **Right-size memory**: Don't over-allocate
3. **Implement caching**: Reduce unnecessary invocations
4. **Use HTTP API**: Always-free tier vs REST API 12-month limit
5. **Monitor usage**: Set up billing alerts
6. **Batch processing**: Process multiple items per invocation
7. **Use S3 events wisely**: Each event triggers an invocation
8. **Optimize cold starts**: Faster initialization = less compute time

## Example: Staying Under Free Tier

```
Goal: Run completely free for 1 year

Strategy:
- Use HTTP API (always free for 1M calls)
- Optimize Lambda to 100ms duration at 256MB
- Limit to 800K requests/month

Monthly Usage:
- Requests: 800K (under 1M) ✅
- GB-seconds: 800K × 0.1s × 0.25GB = 20,000 (under 400K) ✅
- API calls: 800K (under 1M) ✅

Result: $0.00/month indefinitely! 🎉
```

## Additional Free Tier Services

These AWS services also have free tiers that work well with Lambda:

- **DynamoDB**: 25 GB storage, 25 WCU, 25 RCU (always free)
- **SNS**: 1M publishes (always free)
- **SQS**: 1M requests (always free)
- **CloudWatch**: 5GB logs, 3 dashboards (always free)
- **S3**: 5 GB storage (12 months for new accounts)

## Related Documentation
- AWS Free Tier FAQs
- Lambda Pricing Calculator
- AWS Budgets Setup
- Cost Optimization Guide

