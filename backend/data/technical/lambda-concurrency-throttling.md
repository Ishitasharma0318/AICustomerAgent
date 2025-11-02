---
category: technical
subcategory: performance
service: lambda
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/invocation-scaling.html
---

# Lambda Concurrency and Throttling Issues

## Overview
Lambda throttling occurs when concurrent executions exceed limits. Understanding concurrency helps prevent throttling and ensures reliability.

## Concurrency Limits

### Account Limits
- **Default**: 1,000 concurrent executions per region
- **Can be increased**: Request limit increase via AWS Support

### Reserved Concurrency
Set aside concurrency for specific functions

```yaml
Resources:
  CriticalFunction:
    Type: AWS::Serverless::Function
    Properties:
      ReservedConcurrentExecutions: 100  # Guaranteed 100
```

### Provisioned Concurrency
Pre-initialized instances (eliminates cold starts)

```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 10
```

## Throttling Error Messages

### Error 429: TooManyRequestsException
```json
{
  "errorMessage": "Rate Exceeded",
  "errorType": "TooManyRequestsException"
}
```

### CloudWatch Logs
```
START RequestId: xxx Version: $LATEST
END RequestId: xxx
REPORT RequestId: xxx Duration: 1.00 ms
Throttles: 5  ← Throttling occurred!
```

## How Throttling Works

```
Available Concurrency = Account Limit - Reserved Concurrency (all functions)

Example:
- Account limit: 1,000
- Function A reserved: 200
- Function B reserved: 300
- Available for others: 500
```

## Diagnosing Throttling

### Check CloudWatch Metrics
```bash
# Get throttle count
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Throttles \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time 2024-11-01T00:00:00Z \
  --end-time 2024-11-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### Check Concurrent Executions
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name ConcurrentExecutions \
  --dimensions Name=FunctionName,Value=my-function \
  --statistics Maximum
```

## Solutions

### 1. Increase Account Limit
```bash
# Request limit increase via AWS Support
# Can go up to tens of thousands
```

### 2. Use Reserved Concurrency
```python
# Ensure critical functions have guaranteed capacity
aws lambda put-function-concurrency \
  --function-name critical-function \
  --reserved-concurrent-executions 100
```

### 3. Implement Retry Logic
```python
import boto3
from botocore.exceptions import ClientError
import time

lambda_client = boto3.client('lambda')

def invoke_with_retry(function_name, payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=payload
            )
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'TooManyRequestsException':
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = (2 ** attempt) + random.random()
                    time.sleep(wait_time)
                    continue
            raise
```

### 4. Use SQS for Rate Limiting
```
High traffic → SQS Queue → Lambda (controlled concurrency)
```

```yaml
Resources:
  MyQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 300
  
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      ReservedConcurrentExecutions: 50  # Limit processing rate
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt MyQueue.Arn
            BatchSize: 10
```

### 5. Optimize Function Duration
Faster execution = higher throughput with same concurrency

```python
# ❌ Slow (uses concurrency longer)
def slow_handler(event, context):
    time.sleep(5)  # Unnecessary wait
    return process(event)

# ✅ Fast (frees concurrency quickly)
def fast_handler(event, context):
    return process(event)  # No artificial delays
```

## Monitoring Concurrency

### CloudWatch Dashboard
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/Lambda", "ConcurrentExecutions"],
          [".", "Throttles"],
          [".", "Invocations"]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Lambda Concurrency"
      }
    }
  ]
}
```

### Alarms
```bash
# Alert on throttles
aws cloudwatch put-metric-alarm \
  --alarm-name lambda-throttling \
  --alarm-description "Lambda function throttled" \
  --metric-name Throttles \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1
```

## Burst Concurrency

Lambda can burst to:
- **Initial burst**: 3,000 concurrent executions
- **Sustained burst**: +500 per minute until account limit

## Best Practices

1. **Monitor concurrency metrics** regularly
2. **Set reserved concurrency** for critical functions
3. **Use SQS** for high-volume async processing
4. **Implement retry logic** with exponential backoff
5. **Optimize function duration** to free concurrency faster
6. **Request limit increases** proactively
7. **Test under load** to find limits
8. **Use provisioned concurrency** for predictable traffic

## Cost Considerations

### Reserved Concurrency
- **Cost**: Free! Only pay for actual invocations
- **Trade-off**: Reduces available concurrency for other functions

### Provisioned Concurrency
- **Cost**: $0.0000041667 per GB-second
- **Benefit**: No cold starts, guaranteed capacity
- **Use case**: Latency-critical, predictable traffic

## Comparison Table

| Type | Cold Starts | Guaranteed Capacity | Cost |
|------|-------------|-------------------|------|
| On-demand | Yes | No | Cheapest |
| Reserved | Yes | Yes | Same as on-demand |
| Provisioned | No | Yes | Most expensive |

## Related Documentation
- Lambda Scaling
- Concurrency Management
- SQS Integration
- Performance Optimization

