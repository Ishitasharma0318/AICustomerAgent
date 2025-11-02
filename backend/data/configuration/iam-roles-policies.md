---
category: configuration
subcategory: security
service: iam
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
---

# IAM Roles and Policies for Lambda and API Gateway

## Overview
Proper IAM configuration is critical for Lambda and API Gateway security. This guide covers execution roles, resource policies, and best practices.

## Lambda Execution Role

### What is it?
An IAM role that Lambda assumes when executing your function. It determines what AWS services your function can access.

### Basic Execution Role
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### Common Permissions by Use Case

#### 1. DynamoDB Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:region:account-id:table/TableName"
    }
  ]
}
```

#### 2. S3 Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::my-bucket"
    }
  ]
}
```

#### 3. SQS Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:region:account-id:queue-name"
    }
  ]
}
```

#### 4. VPC Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface"
      ],
      "Resource": "*"
    }
  ]
}
```

## API Gateway Permissions

### Allow API Gateway to Invoke Lambda
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
      "Resource": "arn:aws:lambda:region:account-id:function:function-name",
      "Condition": {
        "ArnLike": {
          "AWS:SourceArn": "arn:aws:execute-api:region:account-id:api-id/*"
        }
      }
    }
  ]
}
```

### Using SAM (Automatic Permission)
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Events:
        ApiEvent:
          Type: HttpApi  # Automatically creates permission
          Properties:
            Path: /hello
            Method: get
```

## Best Practices

### 1. Principle of Least Privilege
```json
// ❌ BAD - Too permissive
{
  "Effect": "Allow",
  "Action": "dynamodb:*",
  "Resource": "*"
}

// ✅ GOOD - Specific permissions
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem"
  ],
  "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/SpecificTable"
}
```

### 2. Use Managed Policies When Appropriate
```yaml
Resources:
  MyFunctionRole:
    Type: AWS::IAM::Role
    Properties:
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
        - arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
```

### 3. Resource-Specific Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/public/*",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/environment": "production"
        }
      }
    }
  ]
}
```

### 4. Use Policy Conditions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "dynamodb:PutItem",
      "Resource": "*",
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": ["${aws:username}"]
        }
      }
    }
  ]
}
```

## Common IAM Issues

### Issue 1: AccessDeniedException
**Symptom**: Lambda can't access AWS service
**Solution**: Add required permissions to execution role

### Issue 2: API Gateway 403 Error
**Symptom**: API Gateway can't invoke Lambda
**Solution**: Add resource-based policy to Lambda

```bash
# Add permission using AWS CLI
aws lambda add-permission \
  --function-name my-function \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:region:account-id:api-id/*"
```

### Issue 3: VPC-Related Timeouts
**Symptom**: Lambda in VPC can't access internet/AWS services
**Solution**: Ensure NAT Gateway or VPC endpoints configured

## Complete Example: Lambda with Multiple Services

```yaml
# SAM Template
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: python3.11
      Policies:
        # CloudWatch Logs (automatically included)
        - AWSLambdaBasicExecutionRole
        
        # DynamoDB access
        - DynamoDBCrudPolicy:
            TableName: !Ref MyTable
        
        # S3 read access
        - S3ReadPolicy:
            BucketName: !Ref MyBucket
        
        # SQS send message
        - SQSSendMessagePolicy:
            QueueName: !GetAtt MyQueue.QueueName
        
        # Custom policy
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - secretsmanager:GetSecretValue
              Resource: !Ref MySecret
```

## Security Checklist

- [ ] Use least privilege principle
- [ ] Specify exact resources (avoid `*`)
- [ ] Use conditions to further restrict access
- [ ] Rotate credentials regularly
- [ ] Enable CloudTrail for audit logs
- [ ] Use AWS Secrets Manager for sensitive data
- [ ] Review permissions periodically
- [ ] Use separate roles for dev/staging/prod
- [ ] Enable MFA for sensitive operations
- [ ] Use VPC endpoints for AWS service access

## Troubleshooting Commands

```bash
# Get function's execution role
aws lambda get-function --function-name my-function \
  --query 'Configuration.Role'

# Get role's policies
aws iam list-attached-role-policies --role-name my-role

# Get inline policies
aws iam list-role-policies --role-name my-role

# Simulate policy
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/my-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

## Related Documentation
- IAM Best Practices
- Lambda Security
- API Gateway Authorization
- AWS Secrets Manager

