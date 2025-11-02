---
category: configuration
subcategory: best_practices
service: api-gateway
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html
---

# API Gateway Request Validation

## Overview
Request validation in API Gateway helps reject invalid requests before they reach your Lambda function, saving costs and improving security.

## Why Validate at API Gateway?

**Benefits**:
- Reduce Lambda invocations (save money)
- Faster response to invalid requests
- Consistent validation across APIs
- Reduce Lambda code complexity

## Request Validation Options

### 1. Validate Request Body
```yaml
Resources:
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      Models:
        UserModel:
          type: object
          required:
            - email
            - name
          properties:
            email:
              type: string
              format: email
            name:
              type: string
              minLength: 1
              maxLength: 100
            age:
              type: integer
              minimum: 0
              maximum: 150
```

### 2. Validate Query Parameters
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Events:
        GetUser:
          Type: Api
          Properties:
            Path: /users
            Method: get
            RequestParameters:
              - method.request.querystring.page:
                  Required: true
                  Caching: false
              - method.request.querystring.limit:
                  Required: false
```

### 3. Validate Headers
```yaml
RequestParameters:
  - method.request.header.Authorization:
      Required: true
  - method.request.header.Content-Type:
      Required: true
```

## JSON Schema Examples

### Simple User Schema
```json
{
  "type": "object",
  "required": ["email", "password"],
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 255
    },
    "password": {
      "type": "string",
      "minLength": 8,
      "maxLength": 100
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 120
    }
  }
}
```

### Complex Nested Schema
```json
{
  "type": "object",
  "required": ["user", "items"],
  "properties": {
    "user": {
      "type": "object",
      "required": ["id", "name"],
      "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"}
      }
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["productId", "quantity"],
        "properties": {
          "productId": {"type": "string"},
          "quantity": {
            "type": "integer",
            "minimum": 1
          }
        }
      },
      "minItems": 1,
      "maxItems": 50
    }
  }
}
```

## HTTP API Validation (Simpler)

```yaml
Resources:
  MyHttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      DefinitionBody:
        openapi: '3.0'
        paths:
          /users:
            post:
              requestBody:
                required: true
                content:
                  application/json:
                    schema:
                      type: object
                      required: [email, name]
                      properties:
                        email:
                          type: string
                          format: email
                        name:
                          type: string
```

## Error Responses

When validation fails, API Gateway returns:

```json
{
  "message": "Invalid request body"
}
```

**Status Code**: 400 Bad Request

## Complete SAM Example

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Models:
        CreateUserModel:
          type: object
          required:
            - email
            - name
          properties:
            email:
              type: string
              format: email
            name:
              type: string
              minLength: 1
            phone:
              type: string
              pattern: '^\+?[1-9]\d{1,14}$'
  
  CreateUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.create_user
      Runtime: python3.11
      Events:
        CreateUser:
          Type: Api
          Properties:
            RestApiId: !Ref MyApi
            Path: /users
            Method: post
            RequestModel:
              Model: CreateUserModel
              Required: true
              ValidateBody: true
```

## Best Practices

1. **Validate at Gateway** - Cheaper than Lambda validation
2. **Use JSON Schema** - Standard, well-documented format
3. **Set Limits** - minLength, maxLength, minimum, maximum
4. **Validate Format** - email, date, uuid, etc.
5. **Required Fields** - Explicitly mark required fields
6. **Array Limits** - minItems, maxItems to prevent abuse

## Testing Validation

```bash
# Valid request
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John"}'

# Invalid request (missing required field)
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
# Returns: 400 Bad Request
```

## Related Documentation
- JSON Schema Specification
- OpenAPI 3.0 Specification
- API Gateway Request Validation
- Input Validation Best Practices

