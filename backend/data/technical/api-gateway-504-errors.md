---
category: technical
subcategory: error_handling
service: api-gateway
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html
---

# API Gateway 504 Gateway Timeout Errors

## Overview
A 504 Gateway Timeout error occurs when API Gateway doesn't receive a response from the backend (Lambda or HTTP endpoint) within the timeout period. API Gateway has a maximum integration timeout of 29 seconds.

## Important Limits
- **Maximum API Gateway timeout**: 29 seconds (cannot be increased)
- **Lambda timeout**: Up to 900 seconds (15 minutes)
- **If Lambda runs longer than 29 seconds**: API Gateway returns 504

## Common Causes

1. **Lambda execution exceeds 29 seconds**
2. **Slow database queries**
3. **External API calls taking too long**
4. **Cold start delays** (especially with large deployment packages or VPC)
5. **Network latency** in VPC configurations

## Error Message
```json
{
  "message": "Endpoint request timed out"
}
```

## How to Diagnose

### Step 1: Check Lambda Duration
```bash
# Check CloudWatch Metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time 2024-11-01T00:00:00Z \
  --end-time 2024-11-02T00:00:00Z \
  --period 3600 \
  --statistics Maximum,Average
```

### Step 2: Review CloudWatch Logs
Look for:
- Long execution times
- Slow database queries
- API call durations
- Cold start indicators

### Step 3: Enable X-Ray Tracing
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

@xray_recorder.capture('process_data')
def process_data():
    # Your code here
    pass
```

## Solutions

### 1. Use Asynchronous Invocation
For tasks longer than 29 seconds, use async processing:

**Option A: Asynchronous Lambda Invocation**
```python
# API Gateway Lambda returns immediately
import boto3
import json

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Start long-running task asynchronously
    lambda_client.invoke(
        FunctionName='long-running-function',
        InvocationType='Event',  # Async
        Payload=json.dumps(event)
    )
    
    return {
        'statusCode': 202,  # Accepted
        'body': json.dumps({
            'message': 'Processing started',
            'request_id': context.request_id
        })
    }
```

**Option B: SQS Queue**
```python
import boto3
import json

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    # Send to queue for processing
    sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/123/my-queue',
        MessageBody=json.dumps(event)
    )
    
    return {
        'statusCode': 202,
        'body': json.dumps({'message': 'Queued for processing'})
    }
```

### 2. Optimize Performance
```python
# Connection pooling
import pymysql
from dbutils.pooled_db import PooledDB

# Initialize once (outside handler)
db_pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    host='database.example.com',
    user='user',
    password='pass',
    database='mydb'
)

def lambda_handler(event, context):
    # Reuse connection from pool
    conn = db_pool.connection()
    # ... use connection ...
    conn.close()
```

### 3. Implement Timeout Management
```python
import time

def lambda_handler(event, context):
    # Get remaining time
    remaining_ms = context.get_remaining_time_in_millis()
    
    # Reserve 5 seconds for cleanup and response
    timeout_buffer = 5000
    
    if remaining_ms < timeout_buffer:
        return {
            'statusCode': 503,
            'body': json.dumps({'error': 'Not enough time to process'})
        }
    
    # Process with time awareness
    start_time = time.time()
    max_processing_time = (remaining_ms - timeout_buffer) / 1000
    
    # Your processing logic
    while time.time() - start_time < max_processing_time:
        # Process items
        pass
```

### 4. Use Step Functions for Long Workflows
```yaml
# SAM template for Step Functions
Resources:
  LongRunningWorkflow:
    Type: AWS::Serverless::StateMachine
    Properties:
      Definition:
        StartAt: ProcessData
        States:
          ProcessData:
            Type: Task
            Resource: !GetAtt ProcessFunction.Arn
            TimeoutSeconds: 3600
            End: true
      Policies:
        - LambdaInvokePolicy:
            FunctionName: !Ref ProcessFunction
```

### 5. Reduce Cold Start Impact
- Minimize deployment package size
- Use Lambda layers for dependencies
- Enable Provisioned Concurrency for critical functions
- Consider Lambda SnapStart (for Java)

## Architecture Patterns

### Pattern 1: Immediate Response + Background Processing
```
Client → API Gateway → Lambda (returns 202) → SQS → Worker Lambda
                            ↓
                     DynamoDB (store status)
                            ↑
                     Client polls for status
```

### Pattern 2: Webhook Callback
```
Client → API Gateway → Lambda (starts processing, returns 202)
                            ↓
                     Long-running Lambda
                            ↓
                     HTTP POST to client webhook
```

### Pattern 3: WebSocket for Real-time Updates
```
Client ←→ WebSocket API ← Lambda (sends updates)
                              ↑
                         Processing Lambda
```

## Quick Fixes

### Fix 1: Return Early with Job ID
```python
import uuid
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jobs')

def lambda_handler(event, context):
    job_id = str(uuid.uuid4())
    
    # Save job
    table.put_item(Item={
        'jobId': job_id,
        'status': 'PROCESSING',
        'data': event.get('body')
    })
    
    # Start async processing
    # ... invoke another Lambda or send to SQS ...
    
    return {
        'statusCode': 202,
        'body': json.dumps({
            'jobId': job_id,
            'status': 'PROCESSING',
            'statusUrl': f'/jobs/{job_id}'
        })
    }
```

### Fix 2: Optimize Database Queries
```python
# ❌ BAD - Sequential queries
for item in items:
    result = query_db(item)  # N queries

# ✅ GOOD - Batch query
results = query_db_batch(items)  # 1 query
```

### Fix 3: Parallel Processing
```python
import concurrent.futures

def lambda_handler(event, context):
    items = event['items']
    
    # Process in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_item, items))
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
```

## Prevention Strategies

1. **Set appropriate timeouts**
   - API Gateway Lambda: < 25 seconds recommended
   - Background Lambda: Up to 900 seconds

2. **Monitor duration metrics**
   - Set CloudWatch alarms for duration > 20 seconds
   - Track P99 latency

3. **Use async patterns**
   - Don't make clients wait for long operations
   - Return 202 Accepted with job ID

4. **Optimize cold starts**
   - Keep deployment packages small
   - Use Provisioned Concurrency if needed

5. **Test with realistic loads**
   - Load testing
   - Cold start testing
   - Network latency testing

## Comparison: 502 vs 504

| Error | Cause | Fix |
|-------|-------|-----|
| **502** | Lambda returns invalid response or crashes | Fix response format, add error handling |
| **504** | Lambda exceeds 29 seconds | Use async processing, optimize performance |

## Related Documentation
- AWS Step Functions for long workflows
- SQS for async processing
- Lambda Provisioned Concurrency
- X-Ray for performance tracing

