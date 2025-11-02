---
category: technical
subcategory: error_handling
service: api-gateway
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/apigateway/latest/developerguide/handle-errors-in-lambda-integration.html
---

# API Gateway 502 Bad Gateway Errors

## Overview
A 502 Bad Gateway error in API Gateway indicates that the backend (Lambda function or HTTP endpoint) returned an invalid response or the integration failed.

## Common Causes

### 1. Lambda Function Errors
- Function throws unhandled exceptions
- Function returns improperly formatted response
- Function crashes or times out
- Missing or incorrect IAM permissions

### 2. Integration Configuration Issues
- Incorrect integration request mapping
- Invalid response mapping template
- Missing required headers

### 3. Lambda Response Format Issues
- Response doesn't match expected format
- Missing required fields (statusCode, body)
- Invalid JSON in response body

## Error Scenarios

### Scenario 1: Unhandled Exception in Lambda
```python
# ❌ BAD - Unhandled exception causes 502
def lambda_handler(event, context):
    data = event['body']  # KeyError if 'body' doesn't exist
    return {'statusCode': 200}
```

```python
# ✅ GOOD - Proper error handling
def lambda_handler(event, context):
    try:
        data = event.get('body', '{}')
        # Process data
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Scenario 2: Invalid Response Format
```python
# ❌ BAD - Invalid response format
def lambda_handler(event, context):
    return "Just a string"  # Causes 502

# ✅ GOOD - Correct format for API Gateway
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'Success'})
    }
```

## How to Diagnose

### Step 1: Check CloudWatch Logs
1. Go to Lambda function's CloudWatch Logs
2. Look for error messages or stack traces
3. Check if function completed successfully

### Step 2: Enable API Gateway Logging
```bash
# Enable execution logging
aws apigateway update-stage \
  --rest-api-id abc123 \
  --stage-name prod \
  --patch-operations \
    op=replace,path=/*/logging/loglevel,value=INFO
```

### Step 3: Check Lambda Permissions
Verify API Gateway has permission to invoke Lambda:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:region:account:function:function-name"
    }
  ]
}
```

## Solutions

### 1. Fix Lambda Response Format
Always return this structure:
```python
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,  # Required
        'headers': {        # Optional but recommended
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({  # Required, must be string
            'message': 'Success'
        })
    }
```

### 2. Add Error Handling
```python
import json
import traceback

def lambda_handler(event, context):
    try:
        # Your business logic
        result = process_request(event)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except ValueError as e:
        # Client error
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input', 'details': str(e)})
        }
    except Exception as e:
        # Server error
        print(f"Error: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

### 3. Validate Integration Configuration
**For Lambda Proxy Integration** (Recommended):
- API Gateway passes entire request to Lambda
- Lambda must return proper format
- No mapping templates needed

**For Lambda Integration** (Custom):
- Requires integration request/response templates
- More complex but offers more control

### 4. Test Lambda Function Independently
```bash
# Test Lambda directly
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  response.json

# Check response
cat response.json
```

## Common Mistakes

### Mistake 1: Returning Wrong Type
```python
# ❌ Wrong
return [1, 2, 3]  # List causes 502

# ✅ Correct
return {
    'statusCode': 200,
    'body': json.dumps([1, 2, 3])
}
```

### Mistake 2: Not Stringifying Body
```python
# ❌ Wrong
return {
    'statusCode': 200,
    'body': {'key': 'value'}  # Object causes 502
}

# ✅ Correct
return {
    'statusCode': 200,
    'body': json.dumps({'key': 'value'})  # String
}
```

### Mistake 3: Missing CORS Headers
```python
# Add CORS headers if calling from browser
return {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    },
    'body': json.dumps(data)
}
```

## Testing Checklist

- [ ] Lambda function returns correct format
- [ ] Error handling catches all exceptions
- [ ] CloudWatch Logs show successful execution
- [ ] IAM permissions are correctly configured
- [ ] Integration type is set correctly (Proxy vs Custom)
- [ ] Response body is JSON stringified
- [ ] CORS headers included if needed

## Quick Fix Template

```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Your logic here
        result = {'message': 'Success'}
        
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
        logger.info(f"Returning response: {json.dumps(response)}")
        return response
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal server error'})
        }
```

## Related Errors
- 504 Gateway Timeout
- 500 Internal Server Error
- 403 Forbidden (permission issues)

