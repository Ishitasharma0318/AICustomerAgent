---
category: billing
subcategory: pricing
service: lambda
difficulty: beginner
last_updated: 2024-11-02
source: https://aws.amazon.com/lambda/pricing/
---

# AWS Regional Pricing Differences

## Overview
Lambda and API Gateway pricing varies by AWS region. Understanding these differences helps optimize costs for global applications.

## Lambda Pricing by Region (x86)

### US Regions
| Region | Request Price | Duration (per GB-sec) |
|--------|--------------|---------------------|
| us-east-1 (N. Virginia) | $0.20/M | $0.0000166667 |
| us-east-2 (Ohio) | $0.20/M | $0.0000166667 |
| us-west-1 (N. California) | $0.20/M | $0.0000185185 |
| us-west-2 (Oregon) | $0.20/M | $0.0000166667 |

### Europe Regions
| Region | Request Price | Duration (per GB-sec) |
|--------|--------------|---------------------|
| eu-west-1 (Ireland) | $0.20/M | $0.0000166667 |
| eu-west-2 (London) | $0.20/M | $0.0000175926 |
| eu-central-1 (Frankfurt) | $0.20/M | $0.0000185185 |

### Asia Pacific Regions
| Region | Request Price | Duration (per GB-sec) |
|--------|--------------|---------------------|
| ap-south-1 (Mumbai) | $0.20/M | $0.0000185185 |
| ap-southeast-1 (Singapore) | $0.20/M | $0.0000185185 |
| ap-northeast-1 (Tokyo) | $0.20/M | $0.0000185185 |

## API Gateway Pricing by Region

### HTTP API
| Region | Price per Million |
|--------|------------------|
| us-east-1 | $1.00 |
| us-west-2 | $1.00 |
| eu-west-1 | $1.00 |
| ap-southeast-1 | $1.13 |

### REST API
| Region | Price per Million |
|--------|------------------|
| us-east-1 | $3.50 |
| us-west-2 | $3.50 |
| eu-west-1 | $3.50 |
| ap-southeast-1 | $3.94 |

## Cost Comparison Example

### Same Workload, Different Regions

**Workload**: 10M requests/month, 200ms duration, 512MB

**us-east-1** (Cheapest):
```
Requests: 10M × $0.20/M = $2.00
Duration: 10M × 0.2s × 0.5GB × $0.0000166667 = $16.67
API (HTTP): 10M × $1.00/M = $10.00
Total: $28.67/month
```

**eu-central-1** (More Expensive):
```
Requests: 10M × $0.20/M = $2.00
Duration: 10M × 0.2s × 0.5GB × $0.0000185185 = $18.52
API (HTTP): 10M × $1.00/M = $10.00
Total: $30.52/month

Difference: +$1.85/month (+6.4%)
```

**ap-southeast-1** (Most Expensive):
```
Requests: 10M × $0.20/M = $2.00
Duration: 10M × 0.2s × 0.5GB × $0.0000185185 = $18.52
API (HTTP): 10M × $1.13/M = $11.30
Total: $31.82/month

Difference: +$3.15/month (+11%)
```

## When Regional Pricing Matters

### ✅ Choose Cheaper Region If:
- Application is not latency-sensitive
- Users are globally distributed
- Costs are significant (>$1000/month)
- No data residency requirements

### ❌ Don't Optimize for Price If:
- Latency is critical
- Data must stay in specific region (compliance)
- Cost difference is minimal (<5%)
- Users concentrated in one region

## Multi-Region Strategy

### Pattern 1: Primary + Failover
```yaml
# Deploy primarily in us-east-1 (cheapest)
# Failover to us-west-2 if needed

Resources:
  PrimaryFunction:
    Type: AWS::Serverless::Function
    Properties:
      # us-east-1 configuration
  
  FailoverFunction:
    Type: AWS::Serverless::Function
    Properties:
      # us-west-2 configuration
```

### Pattern 2: Regional Routing
```
Users in:
- North America → us-east-1
- Europe → eu-west-1
- Asia → ap-southeast-1

Use Route 53 latency-based routing
```

## Data Transfer Costs

Often more significant than compute costs!

### Internet Data Transfer Out
| Region | First 10 TB/month |
|--------|------------------|
| us-east-1 | $0.09/GB |
| us-west-1 | $0.09/GB |
| eu-west-1 | $0.09/GB |
| ap-southeast-1 | $0.12/GB |

### Cross-Region Data Transfer
$0.02/GB between regions in same continent
$0.02-0.05/GB between continents

## Optimization Tips

### 1. Start in us-east-1
Cheapest for most services

### 2. Consider Data Transfer
Often bigger cost than compute

### 3. Use CloudFront
Reduces data transfer costs

### 4. Consolidate Regions
Each additional region adds operational overhead

### 5. Monitor Actual Costs
Use Cost Explorer to see real costs by region

## Free Tier (Same All Regions)

The free tier limits are identical across all regions:
- **Lambda**: 1M requests + 400K GB-seconds
- **API Gateway HTTP**: 1M requests
- **Data Transfer**: 1 GB out to internet

## Cost Calculator by Region

```python
LAMBDA_PRICING = {
    'us-east-1': {'request': 0.20, 'duration': 0.0000166667},
    'us-west-2': {'request': 0.20, 'duration': 0.0000166667},
    'eu-west-1': {'request': 0.20, 'duration': 0.0000166667},
    'eu-central-1': {'request': 0.20, 'duration': 0.0000185185},
    'ap-southeast-1': {'request': 0.20, 'duration': 0.0000185185},
}

def calculate_cost_by_region(region, requests_millions, duration_ms, memory_mb):
    pricing = LAMBDA_PRICING[region]
    
    # Calculate costs
    request_cost = requests_millions * pricing['request']
    gb_seconds = (requests_millions * 1_000_000) * (duration_ms / 1000) * (memory_mb / 1024)
    duration_cost = gb_seconds * pricing['duration']
    
    total = request_cost + duration_cost
    
    return {
        'region': region,
        'request_cost': request_cost,
        'duration_cost': duration_cost,
        'total': total
    }

# Compare regions
regions = ['us-east-1', 'eu-central-1', 'ap-southeast-1']
for region in regions:
    cost = calculate_cost_by_region(region, 10, 200, 512)
    print(f"{region}: ${cost['total']:.2f}/month")
```

## Summary

**Cheapest Regions (Generally)**:
1. us-east-1 (N. Virginia)
2. us-east-2 (Ohio)
3. us-west-2 (Oregon)

**Most Expensive Regions**:
1. Asia Pacific regions (+10-15%)
2. Some Europe regions (+5-10%)
3. Middle East/Africa (+10-20%)

**Recommendation**: Start in us-east-1 unless latency or compliance requires otherwise

## Related Documentation
- AWS Regional Pricing
- Data Transfer Pricing
- Multi-Region Architecture
- CloudFront Pricing

