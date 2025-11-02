---
category: technical
subcategory: error_handling
service: lambda
difficulty: beginner
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html
---

# Lambda Timeout Errors

## Overview
Lambda function timeout errors occur when a function exceeds its configured timeout limit. The default timeout is 3 seconds, but it can be configured up to 15 minutes (900 seconds).

## Common Causes

1. **Inefficient code**: Unoptimized algorithms or unnecessary loops
2. **External API calls**: Slow or unresponsive third-party services
3. **Database queries**: Long-running or inefficient database queries
4. **Cold start overhead**: Initial invocation takes longer due to initialization
5. **Network latency**: Slow network connections, especially in VPC configurations

## Error Message
When a timeout occurs, you'll see this error in CloudWatch Logs:
```
Task timed out after X.XX seconds
```

## How to Diagnose

### Check CloudWatch Logs
1. Go to CloudWatch Logs
2. Find your function's log group
3. Look for timeout error messages
4. Review the duration of recent invocations

### Review Function Duration Metrics
Use CloudWatch metrics to analyze:
- Average duration
- Maximum duration
- P99 duration (99th percentile)

## Solutions

### 1. Increase Timeout Value
Configure timeout in function settings (maximum 900 seconds):

**Using AWS Console:**
- Configuration → General configuration → Edit → Timeout

**Using SAM template:**
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Timeout: 60  # seconds
```

**Using AWS CLI:**
```bash
aws lambda update-function-configuration \
  --function-name my-function \
  --timeout 60
```

### 2. Optimize Code Performance
- Use efficient algorithms and data structures
- Implement connection pooling for databases
- Cache frequently accessed data
- Use async/await for concurrent operations
- Minimize cold start impact by keeping functions warm

### 3. Implement Async Processing
For long-running tasks, consider:
- AWS Step Functions for orchestration
- SQS queues for asynchronous processing
- Split large tasks into smaller chunks

### 4. Database Optimization
- Use connection pooling (reuse connections across invocations)
- Add database indexes
- Optimize queries
- Consider using DynamoDB for faster access

### 5. API Call Optimization
- Set timeouts on external API calls
- Implement circuit breakers
- Use exponential backoff for retries
- Consider caching API responses

## Prevention Tips

### Monitor Duration Metrics
Set up CloudWatch alarms for:
- Duration exceeding 80% of timeout
- Increasing trend in average duration

### Performance Testing
- Test with realistic data volumes
- Simulate production load
- Test cold start scenarios

### Code Best Practices
```python
import time
import boto3
from botocore.config import Config

# Configure SDK timeouts
config = Config(
    connect_timeout=5,
    read_timeout=10,
    retries={'max_attempts': 2}
)

# Reuse connections (initialize outside handler)
dynamodb = boto3.resource('dynamodb', config=config)

def lambda_handler(event, context):
    # Check remaining time
    remaining_time = context.get_remaining_time_in_millis()
    
    if remaining_time < 5000:  # Less than 5 seconds left
        return {
            'statusCode': 503,
            'body': 'Not enough time to process'
        }
    
    # Your logic here
    return {'statusCode': 200}
```

## Common Timeout Values by Use Case

| Use Case | Recommended Timeout |
|----------|---------------------|
| API Gateway integration | 30 seconds |
| Simple data processing | 30-60 seconds |
| File processing | 5-15 minutes |
| Data pipeline | 5-15 minutes |
| Quick queries | 10-30 seconds |

## Related Issues
- Cold start delays
- VPC networking latency
- Database connection timeouts
- Memory limitations (can affect execution speed)

## Additional Resources
- AWS Lambda Execution Environment
- CloudWatch Logs for debugging
- Performance optimization guide
- Asynchronous invocation patterns

