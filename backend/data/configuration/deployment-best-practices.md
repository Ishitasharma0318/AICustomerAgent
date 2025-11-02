---
category: configuration
subcategory: deployment
service: lambda
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/deploying-lambda-apps.html
---

# Lambda Deployment Best Practices

## Overview
Proper deployment practices ensure reliable, consistent Lambda deployments with minimal downtime and easy rollbacks.

## Deployment Tools

### AWS SAM (Recommended)
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: python3.11
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary10Percent5Minutes
```

**Deploy**:
```bash
sam build
sam deploy --guided
```

### AWS CDK
```python
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw
)

class MyStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        fn = _lambda.Function(
            self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda")
        )
```

## Best Practices

### 1. Use Aliases and Versions
```bash
# Publish version
aws lambda publish-version --function-name my-function

# Create/update alias
aws lambda update-alias \
  --function-name my-function \
  --name prod \
  --function-version 5
```

### 2. Implement Blue/Green Deployments
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Linear10PercentEvery1Minute
        Alarms:
          - !Ref MyFunctionErrorAlarm
        Hooks:
          PreTraffic: !Ref PreTrafficHook
          PostTraffic: !Ref PostTrafficHook
```

### 3. Use Environment Variables for Configuration
```yaml
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          STAGE: !Ref Environment
          TABLE_NAME: !Sub "users-${Environment}"
```

### 4. Tag Resources
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Tags:
        Environment: production
        Application: my-app
        ManagedBy: SAM
        CostCenter: engineering
```

### 5. Implement CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy Lambda

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: aws-actions/setup-sam@v1
      - name: SAM Build
        run: sam build
      - name: SAM Deploy
        run: sam deploy --no-confirm-changeset
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## Deployment Strategies

### Canary
Gradually shift traffic to new version
```yaml
DeploymentPreference:
  Type: Canary10Percent5Minutes  # 10% for 5 min, then 100%
```

### Linear
Incrementally increase traffic
```yaml
DeploymentPreference:
  Type: Linear10PercentEvery1Minute  # Add 10% every minute
```

### All-at-Once
Immediate deployment (use with caution)
```yaml
DeploymentPreference:
  Type: AllAtOnce
```

## Rollback Strategy

### Automatic Rollback
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      DeploymentPreference:
        Type: Canary10Percent5Minutes
        Alarms:
          - !Ref ErrorAlarm
          - !Ref ThrottleAlarm
        # Automatically rolls back if alarms trigger
```

### Manual Rollback
```bash
# List versions
aws lambda list-versions-by-function --function-name my-function

# Rollback alias to previous version
aws lambda update-alias \
  --function-name my-function \
  --name prod \
  --function-version 4  # Previous working version
```

## Testing Before Deployment

### Local Testing
```bash
# Test locally with SAM
sam local invoke -e events/event.json

# Start local API
sam local start-api
```

### Integration Testing
```python
# tests/test_integration.py
import boto3
import json

def test_lambda_integration():
    lambda_client = boto3.client('lambda')
    
    # Invoke staging function
    response = lambda_client.invoke(
        FunctionName='my-function:staging',
        Payload=json.dumps({'test': 'data'})
    )
    
    result = json.loads(response['Payload'].read())
    assert result['statusCode'] == 200
```

## Checklist

- [ ] Code reviewed and approved
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Environment variables configured
- [ ] IAM permissions verified
- [ ] Deployment strategy selected
- [ ] Alarms configured for rollback
- [ ] Staging environment tested
- [ ] Rollback plan documented
- [ ] Monitoring dashboard ready

## Related Documentation
- AWS SAM Documentation
- AWS CDK Guide
- CI/CD Best Practices
- Blue/Green Deployments

