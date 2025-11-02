---
category: technical
subcategory: error_handling
service: lambda
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
---

# Lambda Memory Errors and Out of Memory Issues

## Overview
Lambda functions can fail with out-of-memory errors when they exceed their configured memory limit. Understanding and resolving these issues is critical for reliability.

## Error Messages

```
Runtime exited with error: signal: killed
Runtime.ExitError

Fatal error: runtime: out of memory
```

## Memory Limits

- **Minimum**: 128 MB
- **Maximum**: 10,240 MB (10 GB)
- **Increment**: 1 MB
- **Default**: 128 MB (often too low!)

## Common Causes

### 1. Memory Leaks
```python
# ❌ Memory leak - list grows indefinitely
results = []

def lambda_handler(event, context):
    global results
    results.append(process_data(event))  # Never cleared!
    return {'status': 'ok'}
```

###2. Large Data Processing
```python
# ❌ Loading entire file into memory
def lambda_handler(event, context):
    with open('/tmp/large_file.csv', 'r') as f:
        data = f.read()  # Could be GBs!
    process(data)
```

### 3. Inefficient Libraries
```python
# ❌ Heavy libraries
import pandas as pd  # Can use 100+ MB just to import
import numpy as np
```

### 4. Recursive Functions Without Limits
```python
# ❌ Unbounded recursion
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # Stack overflow!
```

## How to Diagnose

### Check CloudWatch Logs
Look for:
```
REPORT RequestId: xxx Duration: 3000.00 ms
Billed Duration: 3000 ms
Memory Size: 512 MB
Max Memory Used: 510 MB  ← Near limit!
```

### Monitor Memory Usage
```python
import psutil
import os

def lambda_handler(event, context):
    process = psutil.Process(os.getpid())
    
    # Before processing
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Your code
    result = process_data(event)
    
    # After processing
    mem_after = process.memory_info().rss / 1024 / 1024
    
    print(f"Memory used: {mem_after - mem_before:.2f} MB")
    print(f"Total memory: {mem_after:.2f} MB")
    
    return result
```

## Solutions

### 1. Increase Memory Allocation
**Quick fix**: Increase memory in function configuration

```yaml
# SAM template
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      MemorySize: 1024  # Increase from 512 to 1024
```

```bash
# AWS CLI
aws lambda update-function-configuration \
  --function-name my-function \
  --memory-size 1024
```

### 2. Stream Data Instead of Loading All
```python
# ✅ Stream processing
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Stream file
    response = s3.get_object(Bucket='my-bucket', Key='large-file.csv')
    
    # Process line by line
    for line in response['Body'].iter_lines():
        process_line(line)  # Only one line in memory at a time
```

### 3. Use Generator Functions
```python
# ✅ Generator - memory efficient
def process_large_dataset(data):
    for item in data:
        result = expensive_operation(item)
        yield result  # Yields one at a time

def lambda_handler(event, context):
    for result in process_large_dataset(event['items']):
        save_result(result)
```

### 4. Clear Variables
```python
# ✅ Explicitly clear large objects
def lambda_handler(event, context):
    large_data = load_large_data()
    
    result = process(large_data)
    
    # Free memory
    del large_data
    import gc
    gc.collect()
    
    return result
```

### 5. Optimize Data Structures
```python
# ❌ Inefficient - stores entire dataset
results = []
for item in million_items:
    results.append(process(item))

# ✅ Efficient - process and discard
for item in million_items:
    result = process(item)
    save_to_db(result)  # Save immediately, don't accumulate
```

### 6. Use Lambda Layers for Dependencies
```yaml
# Reduce deployment package size
Resources:
  MyLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: heavy-dependencies
      ContentUri: layers/
      CompatibleRuntimes:
        - python3.11
  
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Layers:
        - !Ref MyLayer
      MemorySize: 512  # Can use less memory
```

## Memory Optimization Strategies

### Strategy 1: Right-Size Memory
```python
# Test different memory sizes
memory_configs = [128, 256, 512, 1024, 1536, 2048, 3008]

# Find optimal: enough memory but not excessive
# More memory = more CPU, but also more cost
```

### Strategy 2: Lazy Loading
```python
# ❌ Load all at startup
import pandas as pd
import numpy as np
import tensorflow as tf

# ✅ Load only when needed
def lambda_handler(event, context):
    if event['type'] == 'ml':
        import tensorflow as tf
        # Use tensorflow
```

### Strategy 3: Use /tmp Wisely
Lambda provides 512 MB of /tmp storage (can be increased to 10 GB)

```python
# Use /tmp for temporary files
def lambda_handler(event, context):
    # Download to /tmp
    with open('/tmp/tempfile.dat', 'wb') as f:
        f.write(large_data)
    
    # Process from /tmp (not in memory)
    with open('/tmp/tempfile.dat', 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            process_chunk(chunk)
    
    # Clean up
    os.remove('/tmp/tempfile.dat')
```

## Monitoring and Alerts

### CloudWatch Alarm
```bash
# Alert when memory usage exceeds 90%
aws cloudwatch put-metric-alarm \
  --alarm-name lambda-high-memory \
  --alarm-description "Lambda using >90% memory" \
  --metric-name MemoryUtilization \
  --namespace AWS/Lambda \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 90 \
  --comparison-operator GreaterThanThreshold
```

### Custom Metrics
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    import psutil
    process = psutil.Process()
    memory_percent = process.memory_percent()
    
    # Send custom metric
    cloudwatch.put_metric_data(
        Namespace='CustomLambda',
        MetricData=[{
            'MetricName': 'MemoryUsagePercent',
            'Value': memory_percent,
            'Unit': 'Percent'
        }]
    )
```

## Common Patterns

### Pattern 1: Batch Processing with Memory Awareness
```python
def lambda_handler(event, context):
    import psutil
    
    items = event['items']
    batch = []
    max_memory_percent = 80
    
    for item in items:
        batch.append(item)
        
        # Check memory usage
        mem_percent = psutil.Process().memory_percent()
        
        if mem_percent > max_memory_percent:
            # Process current batch and clear
            process_batch(batch)
            batch = []
            gc.collect()
    
    # Process remaining items
    if batch:
        process_batch(batch)
```

### Pattern 2: Pagination
```python
# Instead of loading all records
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MyTable')
    
    # Paginate through results
    response = table.scan(Limit=100)
    
    while True:
        items = response['Items']
        process_items(items)
        
        if 'LastEvaluatedKey' not in response:
            break
            
        response = table.scan(
            Limit=100,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
```

## Memory vs Performance Trade-off

| Memory | CPU Power | Cost | Use Case |
|--------|-----------|------|----------|
| 128 MB | Low | $0.0000000021/ms | Simple tasks |
| 512 MB | Medium | $0.0000000083/ms | API requests |
| 1024 MB | High | $0.0000000167/ms | Data processing |
| 3008 MB | Very High | $0.0000000500/ms | ML inference |

**Note**: More memory = more CPU, which can make your function faster and potentially cheaper overall!

## Testing Memory Requirements

```python
# Load test script
import boto3
import json

lambda_client = boto3.client('lambda')

memory_sizes = [256, 512, 1024, 1536, 2048]
results = []

for memory in memory_sizes:
    # Update function memory
    lambda_client.update_function_configuration(
        FunctionName='my-function',
        MemorySize=memory
    )
    
    # Wait for update
    time.sleep(5)
    
    # Test invocation
    response = lambda_client.invoke(
        FunctionName='my-function',
        Payload=json.dumps(test_payload)
    )
    
    # Parse logs to get memory used
    log_result = response['LogResult']
    # Extract max memory used from logs
    
    results.append({
        'memory': memory,
        'duration': duration,
        'max_memory_used': max_memory,
        'cost': calculate_cost(memory, duration)
    })

# Find optimal configuration
optimal = min(results, key=lambda x: x['cost'])
```

## Prevention Checklist

- [ ] Set memory higher than peak usage (add 20% buffer)
- [ ] Use streaming for large files
- [ ] Implement generators for large datasets
- [ ] Clear variables explicitly
- [ ] Monitor memory usage metrics
- [ ] Set up alerts for high memory usage
- [ ] Test with production-size data
- [ ] Profile memory usage during development
- [ ] Use appropriate data structures
- [ ] Avoid global variables that accumulate data

## Related Issues
- Lambda timeout errors
- Cold start performance
- Cost optimization
- Deployment package size limits

