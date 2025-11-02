---
category: billing
subcategory: pricing
service: cloudwatch
difficulty: beginner
last_updated: 2024-11-02
source: https://aws.amazon.com/cloudwatch/pricing/
---

# CloudWatch Costs for Lambda

## Overview
CloudWatch costs for Lambda include logs, metrics, and alarms. Understanding these costs helps optimize your Lambda spending.

## CloudWatch Pricing

### Logs
- **Ingestion**: $0.50 per GB
- **Storage**: $0.03 per GB/month
- **Free tier**: 5 GB ingestion per month (always free)

### Metrics
- **Standard metrics**: Free
- **Custom metrics**: $0.30 per metric/month
- **High-resolution metrics**: $0.30 per metric/month
- **Free tier**: 10 custom metrics per month

### Alarms
- **Standard alarms**: $0.10 per alarm/month
- **High-resolution alarms**: $0.30 per alarm/month
- **Free tier**: 10 alarms per month

## Cost Examples

### Example 1: Small Application
```
Lambda Function:
- 100,000 invocations/month
- Average logs: 1 KB per invocation
- 5 custom metrics
- 3 alarms

Costs:
- Logs ingestion: (100,000 × 1KB) = 0.095 GB → FREE (under 5GB)
- Logs storage: 0.095 GB × $0.03 = $0.00
- Custom metrics: FREE (under 10)
- Alarms: FREE (under 10)

Total CloudWatch Cost: $0.00
```

### Example 2: Medium Application
```
Lambda Functions (3 functions):
- 5 million invocations/month total
- Average logs: 2 KB per invocation
- 25 custom metrics
- 15 alarms

Costs:
- Logs ingestion: (5M × 2KB) = 9.5 GB
  - Free: 5 GB
  - Paid: 4.5 GB × $0.50 = $2.25
- Logs storage: 9.5 GB × $0.03 = $0.29
- Custom metrics: 25 total
  - Free: 10
  - Paid: 15 × $0.30 = $4.50
- Alarms: 15 total
  - Free: 10
  - Paid: 5 × $0.10 = $0.50

Total CloudWatch Cost: $7.54/month
```

## Cost Optimization Strategies

### 1. Reduce Log Volume
```python
# ❌ Verbose logging
print(f"Processing item: {item}")  # Every invocation
print(f"Step 1 complete")
print(f"Step 2 complete")

# ✅ Conditional logging
import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

if LOG_LEVEL == 'DEBUG':
    print(f"Processing item: {item}")
```

### 2. Set Log Retention
```yaml
Resources:
  MyFunctionLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/lambda/my-function
      RetentionInDays: 7  # Instead of infinite
```

**Retention Options**: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653 days

### 3. Use Structured Logging
```python
import json

def lambda_handler(event, context):
    # Structured logging - easier to query, less verbose
    log_entry = {
        'level': 'INFO',
        'request_id': context.request_id,
        'action': 'process_user',
        'user_id': event.get('user_id')
    }
    print(json.dumps(log_entry))
```

### 4. Sample Logs
```python
import random

def lambda_handler(event, context):
    # Only log 10% of requests
    if random.random() < 0.1:
        print(f"Sampled log: {event}")
```

### 5. Use Log Insights Efficiently
```bash
# Query specific time range (cheaper than full scan)
fields @timestamp, @message
| filter @timestamp > "2024-11-01T00:00:00"
| filter @timestamp < "2024-11-02T00:00:00"
| limit 100
```

## Cost Monitoring

### Track CloudWatch Costs
```bash
# Create budget for CloudWatch
aws budgets create-budget \
  --account-id 123456789012 \
  --budget file://cloudwatch-budget.json
```

**cloudwatch-budget.json**:
```json
{
  "BudgetName": "CloudWatch Monthly",
  "BudgetLimit": {
    "Amount": "10",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {
    "Service": ["Amazon CloudWatch"]
  }
}
```

## Logs vs X-Ray

| Feature | CloudWatch Logs | X-Ray |
|---------|----------------|-------|
| Cost | $0.50/GB | $5.00 per million traces |
| Use Case | Debugging, audit | Performance analysis |
| Storage | $0.03/GB/month | 30 days free, then $1/month for extended |
| Best For | General logging | Tracing requests |

## Free Tier Summary

| Service | Always Free |
|---------|-------------|
| Logs Ingestion | 5 GB/month |
| Custom Metrics | 10 metrics |
| Alarms | 10 alarms |
| API Requests | 1 million |
| Dashboard | 3 dashboards |

## Cost Calculator

```python
def calculate_cloudwatch_costs(
    invocations_per_month,
    avg_log_size_kb,
    retention_days,
    custom_metrics_count=0,
    alarms_count=0
):
    # Logs
    total_logs_gb = (invocations_per_month * avg_log_size_kb) / 1024 / 1024
    ingestion_cost = max(0, (total_logs_gb - 5)) * 0.50  # 5GB free
    
    # Storage (cumulative)
    months = retention_days / 30
    storage_gb = total_logs_gb * months
    storage_cost = storage_gb * 0.03
    
    # Metrics
    metrics_cost = max(0, custom_metrics_count - 10) * 0.30
    
    # Alarms
    alarms_cost = max(0, alarms_count - 10) * 0.10
    
    total = ingestion_cost + storage_cost + metrics_cost + alarms_cost
    
    return {
        'logs_ingestion': ingestion_cost,
        'logs_storage': storage_cost,
        'metrics': metrics_cost,
        'alarms': alarms_cost,
        'total_monthly': total,
        'total_annual': total * 12
    }

# Example
costs = calculate_cloudwatch_costs(
    invocations_per_month=1_000_000,
    avg_log_size_kb=2,
    retention_days=30,
    custom_metrics_count=15,
    alarms_count=5
)

print(f"Monthly CloudWatch cost: ${costs['total_monthly']:.2f}")
```

## Best Practices Summary

- [ ] Set appropriate log retention (7-30 days typical)
- [ ] Use conditional logging based on environment
- [ ] Implement structured logging
- [ ] Sample high-volume logs
- [ ] Monitor CloudWatch costs
- [ ] Use free tier efficiently
- [ ] Delete old log groups
- [ ] Review custom metrics regularly
- [ ] Consolidate similar alarms
- [ ] Use Log Insights for queries (not exports)

## Related Documentation
- CloudWatch Logs Pricing
- Log Retention Policies
- X-Ray Pricing
- Cost Optimization Guide

