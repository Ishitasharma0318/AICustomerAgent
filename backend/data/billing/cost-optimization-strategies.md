---
category: billing
subcategory: optimization
service: lambda
difficulty: intermediate
last_updated: 2024-11-02
source: https://aws.amazon.com/lambda/pricing/
---

# Lambda and API Gateway Cost Optimization Strategies

## Overview
This guide covers proven strategies to reduce AWS Lambda and API Gateway costs while maintaining performance and reliability.

## Cost Components

### Lambda Costs
1. **Requests**: $0.20 per million requests
2. **Duration**: $0.0000166667 per GB-second (x86) or $0.0000133334 (ARM/Graviton2)
3. **Ephemeral storage** (over 512MB): $0.0000000309 per GB-second
4. **Provisioned concurrency**: $0.0000041667 per GB-second

### API Gateway Costs
1. **REST API**: $3.50 per million requests
2. **HTTP API**: $1.00 per million requests (71% cheaper!)
3. **WebSocket API**: $1.00 per million messages
4. **Caching**: $0.02 per hour for 0.5GB cache

## Top 10 Cost Optimization Strategies

### 1. Use ARM/Graviton2 Architecture
**Savings**: Up to 20% on compute costs

```yaml
# SAM Template
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Architectures:
        - arm64  # Instead of x86_64
      Runtime: python3.11
```

**Cost Comparison**:
- x86: $0.0000166667 per GB-second
- ARM: $0.0000133334 per GB-second
- **Savings**: 20% on duration costs

### 2. Switch from REST API to HTTP API
**Savings**: 71% on API costs

**When to use HTTP API**:
- Simple proxying to Lambda
- No need for API keys
- No need for request validation
- OAuth 2.0 or JWT authorization is sufficient

**Migration Example**:
```yaml
# Before: REST API
Resources:
  MyRestApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      # Costs: $3.50 per million

# After: HTTP API
Resources:
  MyHttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod
      # Costs: $1.00 per million (71% cheaper!)
```

### 3. Right-size Lambda Memory
**Savings**: 20-40% on duration costs

Memory affects both CPU and cost. Finding the sweet spot is crucial.

**Testing Script**:
```python
# Test different memory sizes
memory_sizes = [128, 256, 512, 1024, 1536, 2048, 3008]

for memory in memory_sizes:
    # Update function memory
    # Run load test
    # Calculate: (duration * memory_gb) * cost_per_gb_second
    # Find minimum cost
```

**Rule of Thumb**:
- **CPU-intensive**: More memory = faster = often cheaper
- **I/O-intensive**: Lower memory often sufficient
- **Sweet spot**: Often 512MB - 1024MB

### 4. Reduce Cold Starts (Saves Duration Costs)
**Strategies**:
- Minimize deployment package size
- Remove unused dependencies
- Use Lambda layers for shared code
- Keep functions warm with CloudWatch Events (for critical endpoints)

```python
# Optimize imports
# ❌ Import entire library
import pandas as pd  # Heavy!

# ✅ Import only what you need
from pandas import DataFrame
```

### 5. Connection Pooling
**Savings**: 50-80% on database-heavy functions

```python
# ❌ BAD - Creates new connection every invocation
def lambda_handler(event, context):
    conn = pymysql.connect(host='db', user='user', password='pass')
    # ... use connection ...
    conn.close()

# ✅ GOOD - Reuse connection across invocations
import pymysql

# Initialize outside handler (reused across invocations)
conn = pymysql.connect(
    host='db',
    user='user', 
    password='pass',
    autocommit=True
)

def lambda_handler(event, context):
    # Reuse existing connection
    cursor = conn.cursor()
    # ... use connection ...
```

### 6. Implement Caching
**Multiple caching layers**:

**Layer 1: API Gateway Caching**
```yaml
# SAM Template
Resources:
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      CacheClusterEnabled: true
      CacheClusterSize: '0.5'  # GB
      MethodSettings:
        - ResourcePath: /items
          HttpMethod: GET
          CachingEnabled: true
          CacheTtlInSeconds: 300  # 5 minutes
```

**Cost-Benefit Analysis**:
- Cache cost: $0.02/hour = $14.40/month
- If prevents 1 million Lambda invocations/month:
  - Saves: ~$50-100/month
  - **Net savings**: $35-85/month

**Layer 2: Application-level Caching**
```python
import json
from functools import lru_cache

# Cache in memory (persists across warm invocations)
@lru_cache(maxsize=100)
def get_config(key):
    # Expensive operation
    return fetch_from_dynamodb(key)

def lambda_handler(event, context):
    config = get_config('my-config')  # Cached!
```

### 7. Batch Processing
**Savings**: Up to 90% on request costs

```python
# ❌ BAD - Individual invocations
for item in items:
    invoke_lambda(item)  # 1000 items = 1000 invocations

# ✅ GOOD - Batch processing
batches = chunk_items(items, batch_size=100)
for batch in batches:
    invoke_lambda(batch)  # 1000 items = 10 invocations
```

### 8. Use SQS for Async Processing
**Saves Lambda idle time costs**

```python
# ❌ BAD - Lambda waits for slow operation
def lambda_handler(event, context):
    process_immediately(event)  # Takes 5 minutes
    # You pay for 5 minutes of Lambda time

# ✅ GOOD - Queue for async processing
import boto3
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    sqs.send_message(
        QueueUrl='my-queue',
        MessageBody=json.dumps(event)
    )
    # Returns in milliseconds
    # Worker Lambda processes from queue
```

### 9. Optimize Ephemeral Storage
**Default**: 512 MB free  
**Additional storage**: $0.0000000309 per GB-second

```yaml
# Only increase if needed
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      EphemeralStorage:
        Size: 512  # MB (free tier)
        # Size: 10240  # Costs extra!
```

### 10. Monitor and Set Budgets
**Prevent cost surprises**:

```bash
# Set budget alert
aws budgets create-budget \
  --account-id 123456789012 \
  --budget file://budget.json
```

**budget.json**:
```json
{
  "BudgetName": "Lambda Monthly Budget",
  "BudgetLimit": {
    "Amount": "100",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

## Cost Calculation Examples

### Example 1: Basic API (Before Optimization)
```
Monthly stats:
- 10 million API requests (REST API)
- Lambda: 200ms average, 512MB memory
- No caching

Costs:
- API Gateway: 10M × $3.50/M = $35.00
- Lambda requests: 10M × $0.20/M = $2.00
- Lambda duration: 10M × 0.2s × 0.5GB × $0.0000166667 = $16.67

Total: $53.67/month
```

### Example 2: Optimized API (After Optimization)
```
Changes:
- Switched to HTTP API
- Used ARM architecture
- Added caching (50% hit rate)

Costs:
- API Gateway: 10M × $1.00/M = $10.00 (71% savings!)
- Cache: $14.40/month
- Lambda requests: 5M × $0.20/M = $1.00 (50% fewer due to cache)
- Lambda duration: 5M × 0.2s × 0.5GB × $0.0000133334 = $6.67 (ARM 20% cheaper)

Total: $32.07/month
SAVINGS: $21.60/month (40% reduction!)
```

## Cost Monitoring Dashboard

**Key Metrics to Track**:
1. Lambda invocations per day
2. Average duration
3. Memory utilization
4. API Gateway request count
5. Cache hit rate (if applicable)

**CloudWatch Dashboard**:
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Create cost monitoring dashboard
dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["AWS/Lambda", "Invocations", {"stat": "Sum"}],
                    ["AWS/Lambda", "Duration", {"stat": "Average"}],
                    ["AWS/ApiGateway", "Count", {"stat": "Sum"}]
                ],
                "period": 300,
                "stat": "Average",
                "region": "us-east-1",
                "title": "Cost Drivers"
            }
        }
    ]
}
```

## Quick Wins Checklist

- [ ] Switch to HTTP API (if possible) - **71% API savings**
- [ ] Use ARM architecture - **20% compute savings**
- [ ] Implement connection pooling - **50-80% duration savings**
- [ ] Right-size memory allocation - **20-40% savings**
- [ ] Add caching for frequent requests - **Variable, often 50%+**
- [ ] Batch API calls - **Up to 90% request savings**
- [ ] Remove unused dependencies - **Faster cold starts**
- [ ] Set up cost alerts - **Prevent surprises**

## ROI Calculator

```python
def calculate_savings(
    monthly_requests_millions,
    avg_duration_ms,
    memory_mb,
    current_api_type='rest',
    use_caching=False,
    cache_hit_rate=0.5
):
    # Current costs
    api_cost_rest = monthly_requests_millions * 3.50
    api_cost_http = monthly_requests_millions * 1.00
    
    # Lambda costs (x86)
    request_cost = monthly_requests_millions * 0.20
    duration_cost_x86 = (
        monthly_requests_millions * 1_000_000 *
        (avg_duration_ms / 1000) *
        (memory_mb / 1024) *
        0.0000166667
    )
    
    # Optimized costs (ARM + HTTP API + caching)
    if use_caching:
        effective_requests = monthly_requests_millions * (1 - cache_hit_rate)
        cache_cost = 14.40  # Monthly cost for 0.5GB cache
    else:
        effective_requests = monthly_requests_millions
        cache_cost = 0
    
    duration_cost_arm = duration_cost_x86 * 0.8  # 20% cheaper
    
    # Calculate totals
    current_total = api_cost_rest + request_cost + duration_cost_x86
    optimized_total = (
        api_cost_http +
        (effective_requests * 0.20) +
        (duration_cost_arm * (effective_requests / monthly_requests_millions)) +
        cache_cost
    )
    
    savings = current_total - optimized_total
    savings_percent = (savings / current_total) * 100
    
    return {
        'current': current_total,
        'optimized': optimized_total,
        'monthly_savings': savings,
        'annual_savings': savings * 12,
        'savings_percent': savings_percent
    }

# Example
result = calculate_savings(
    monthly_requests_millions=10,
    avg_duration_ms=200,
    memory_mb=512,
    use_caching=True,
    cache_hit_rate=0.5
)

print(f"Monthly savings: ${result['monthly_savings']:.2f} ({result['savings_percent']:.1f}%)")
print(f"Annual savings: ${result['annual_savings']:.2f}")
```

## Additional Resources
- AWS Cost Explorer
- AWS Budgets
- Lambda Power Tuning Tool
- CloudWatch Cost and Usage Reports

