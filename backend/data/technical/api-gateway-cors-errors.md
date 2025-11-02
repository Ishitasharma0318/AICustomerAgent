---
category: technical
subcategory: error_handling
service: api-gateway
difficulty: beginner
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
---

# API Gateway CORS Errors

## Overview
CORS (Cross-Origin Resource Sharing) errors occur when browsers block requests from web applications to API Gateway due to security policies.

## Common Error Messages

```
Access to fetch at 'https://api.example.com' from origin 'https://myapp.com' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is 
present on the requested resource.
```

## Quick Fix for Lambda

Add CORS headers to Lambda response:

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # or specific domain
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps({'message': 'Success'})
    }
```

## API Gateway CORS Configuration

### HTTP API (Recommended - Simple)
```yaml
Resources:
  MyHttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      CorsConfiguration:
        AllowOrigins:
          - "https://myapp.com"
        AllowHeaders:
          - Content-Type
          - Authorization
        AllowMethods:
          - GET
          - POST
          - OPTIONS
        MaxAge: 300
```

### REST API
```yaml
Resources:
  MyRestApi:
    Type: AWS::Serverless::Api
    Properties:
      Cors:
        AllowMethods: "'GET,POST,OPTIONS'"
        AllowHeaders: "'Content-Type,Authorization'"
        AllowOrigin: "'https://myapp.com'"
```

## Handle OPTIONS Requests

Browsers send OPTIONS (preflight) requests before actual requests:

```python
def lambda_handler(event, context):
    # Handle OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': ''
        }
    
    # Handle actual request
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'data': 'response'})
    }
```

## Security Considerations

### ❌ Don't Use '*' in Production
```python
# Insecure - allows any website
'Access-Control-Allow-Origin': '*'
```

### ✅ Use Specific Origins
```python
# Secure - only allow specific domains
allowed_origins = ['https://myapp.com', 'https://app.example.com']
origin = event['headers'].get('origin', '')

if origin in allowed_origins:
    headers['Access-Control-Allow-Origin'] = origin
```

## Complete CORS Handler Example

```python
import json

ALLOWED_ORIGINS = [
    'https://myapp.com',
    'https://app.example.com'
]

def get_cors_headers(origin):
    """Get CORS headers based on origin"""
    headers = {
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Api-Key',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Max-Age': '300'
    }
    
    # Check if origin is allowed
    if origin in ALLOWED_ORIGINS:
        headers['Access-Control-Allow-Origin'] = origin
    else:
        headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS[0]
    
    return headers

def lambda_handler(event, context):
    origin = event['headers'].get('origin', '')
    cors_headers = get_cors_headers(origin)
    
    # Handle preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    # Handle actual request
    try:
        # Your business logic
        result = process_request(event)
        
        return {
            'statusCode': 200,
            'headers': {**cors_headers, 'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }
```

## Testing CORS

```bash
# Test from browser console
fetch('https://api.example.com/endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({data: 'test'})
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('CORS Error:', error));
```

## Troubleshooting Checklist

- [ ] CORS headers present in Lambda response
- [ ] OPTIONS method handled
- [ ] AllowOrigin matches request origin
- [ ] AllowHeaders includes all required headers
- [ ] AllowMethods includes request method
- [ ] API Gateway CORS configured
- [ ] No conflicting headers
- [ ] Testing from correct origin

## Related Documentation
- CORS specification
- API Gateway CORS configuration
- Browser security policies

