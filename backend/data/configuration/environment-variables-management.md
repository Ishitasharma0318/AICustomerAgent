---
category: configuration
subcategory: best_practices
service: lambda
difficulty: beginner
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
---

# Environment Variables Management in Lambda

## Overview
Environment variables allow you to configure Lambda functions without changing code. This guide covers best practices for managing environment variables securely and efficiently.

## Basic Usage

### Setting Environment Variables

**AWS Console**:
Configuration → Environment variables → Edit

**SAM Template**:
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          TABLE_NAME: users-table
          API_ENDPOINT: https://api.example.com
          LOG_LEVEL: INFO
```

**AWS CLI**:
```bash
aws lambda update-function-configuration \
  --function-name my-function \
  --environment "Variables={TABLE_NAME=users,LOG_LEVEL=INFO}"
```

### Accessing in Code

**Python**:
```python
import os

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    api_endpoint = os.environ.get('API_ENDPOINT', 'default-value')
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    
    print(f"Using table: {table_name}")
```

**Node.js**:
```javascript
exports.handler = async (event) => {
    const tableName = process.env.TABLE_NAME;
    const apiEndpoint = process.env.API_ENDPOINT || 'default';
    const logLevel = process.env.LOG_LEVEL || 'INFO';
    
    console.log(`Using table: ${tableName}`);
};
```

## Best Practices

### 1. Never Store Secrets in Plain Text
```yaml
# ❌ BAD - Plain text secrets
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          DATABASE_PASSWORD: "mysecretpassword123"  # NEVER DO THIS!

# ✅ GOOD - Use AWS Secrets Manager
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          SECRET_ARN: !Ref MySecret
      Policies:
        - AWSSecretsManagerGetSecretValuePolicy:
            SecretArn: !Ref MySecret
```

### 2. Use Parameter Store for Configuration
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          PARAMETER_NAME: /myapp/config/database
      Policies:
        - SSMParameterReadPolicy:
            ParameterName: /myapp/config/*
```

**Fetch at runtime**:
```python
import boto3

ssm = boto3.client('ssm')

def get_parameter(name):
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response['Parameter']['Value']

def lambda_handler(event, context):
    param_name = os.environ['PARAMETER_NAME']
    db_config = get_parameter(param_name)
```

### 3. Separate by Environment
```yaml
# Different environment variables per stage
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]

Mappings:
  EnvironmentConfig:
    dev:
      TableName: users-dev
      LogLevel: DEBUG
    staging:
      TableName: users-staging
      LogLevel: INFO
    prod:
      TableName: users-prod
      LogLevel: ERROR

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          TABLE_NAME: !FindInMap [EnvironmentConfig, !Ref Environment, TableName]
          LOG_LEVEL: !FindInMap [EnvironmentConfig, !Ref Environment, LogLevel]
```

### 4. Use Encryption for Sensitive Data
```yaml
# Encrypt environment variables
Resources:
  MyKMSKey:
    Type: AWS::KMS::Key
    Properties:
      Description: Lambda environment variable encryption
  
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      KmsKeyArn: !GetAtt MyKMSKey.Arn
      Environment:
        Variables:
          SENSITIVE_CONFIG: encrypted-value
```

## Managing Secrets

### Using AWS Secrets Manager
```python
import boto3
import json
from functools import lru_cache

secrets_client = boto3.client('secretsmanager')

@lru_cache(maxsize=1)
def get_secret(secret_arn):
    """Cache secret to avoid repeated API calls"""
    response = secrets_client.get_secret_value(SecretId=secret_arn)
    return json.loads(response['SecretString'])

def lambda_handler(event, context):
    secret_arn = os.environ['SECRET_ARN']
    secret = get_secret(secret_arn)
    
    # Use secret
    db_password = secret['password']
    api_key = secret['api_key']
```

**SAM Template**:
```yaml
Resources:
  MySecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Description: Database credentials
      SecretString: |
        {
          "username": "admin",
          "password": "auto-generated-password"
        }
  
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          SECRET_ARN: !Ref MySecret
      Policies:
        - AWSSecretsManagerGetSecretValuePolicy:
            SecretArn: !Ref MySecret
```

### Using Parameter Store
```python
import boto3
from functools import lru_cache

ssm = boto3.client('ssm')

@lru_cache(maxsize=10)
def get_parameters(path):
    """Get all parameters under a path"""
    response = ssm.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True
    )
    
    return {
        param['Name'].split('/')[-1]: param['Value']
        for param in response['Parameters']
    }

def lambda_handler(event, context):
    config_path = os.environ['CONFIG_PATH']
    config = get_parameters(config_path)
    
    # Access configuration
    db_host = config['db_host']
    db_port = config['db_port']
```

## Common Patterns

### Pattern 1: Feature Flags
```python
import os
import json

def lambda_handler(event, context):
    # Feature flags via environment variables
    features = json.loads(os.environ.get('FEATURE_FLAGS', '{}'))
    
    if features.get('new_algorithm', False):
        return use_new_algorithm(event)
    else:
        return use_old_algorithm(event)
```

### Pattern 2: Dynamic Configuration
```python
import os
import json

def get_config():
    """Load configuration from environment"""
    return {
        'database': {
            'host': os.environ['DB_HOST'],
            'port': int(os.environ.get('DB_PORT', '5432')),
            'name': os.environ['DB_NAME']
        },
        'api': {
            'endpoint': os.environ['API_ENDPOINT'],
            'timeout': int(os.environ.get('API_TIMEOUT', '30')),
            'retries': int(os.environ.get('API_RETRIES', '3'))
        },
        'logging': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'format': os.environ.get('LOG_FORMAT', 'json')
        }
    }

def lambda_handler(event, context):
    config = get_config()
    # Use configuration
```

### Pattern 3: Multi-Region Setup
```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          AWS_REGION_NAME: !Ref AWS::Region
          PRIMARY_REGION: us-east-1
          BACKUP_REGION: us-west-2
```

## Environment Variable Limits

- **Maximum size**: 4 KB for all variables combined
- **Maximum number**: No explicit limit, but total size limited
- **Key length**: 128 characters
- **Value length**: 2048 characters (per variable)

## Security Considerations

### 1. Principle of Least Privilege
```yaml
# Only grant permissions needed
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Policies:
        - Statement:
            - Effect: Allow
              Action:
                - secretsmanager:GetSecretValue
              Resource: !Sub "arn:aws:secretsmanager:${AWS::Region}:${AWS::AccountId}:secret:specific-secret-*"
```

### 2. Rotate Secrets Regularly
```yaml
Resources:
  MySecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Description: Auto-rotated database password
      GenerateSecretString:
        SecretStringTemplate: '{"username": "admin"}'
        GenerateStringKey: password
        PasswordLength: 32
  
  MyRotationSchedule:
    Type: AWS::SecretsManager::RotationSchedule
    Properties:
      SecretId: !Ref MySecret
      RotationLambdaARN: !GetAtt RotationFunction.Arn
      RotationRules:
        AutomaticallyAfterDays: 30
```

### 3. Audit Access
Enable CloudTrail to log access to secrets:
```python
# CloudTrail will log:
# - secretsmanager:GetSecretValue
# - ssm:GetParameter
# - ssm:GetParameters
```

## Testing with Environment Variables

### Local Testing
```bash
# Set environment variables for local testing
export TABLE_NAME=users-dev
export LOG_LEVEL=DEBUG
export AWS_REGION=us-east-1

# Run SAM local
sam local invoke --env-vars env.json
```

**env.json**:
```json
{
  "MyFunction": {
    "TABLE_NAME": "users-dev",
    "LOG_LEVEL": "DEBUG",
    "API_ENDPOINT": "http://localhost:3000"
  }
}
```

### Unit Testing
```python
import pytest
import os

def test_lambda_with_env_vars(monkeypatch):
    # Set environment variables for test
    monkeypatch.setenv('TABLE_NAME', 'test-table')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')
    
    # Import after setting env vars
    from my_function import lambda_handler
    
    result = lambda_handler({}, {})
    assert result['statusCode'] == 200
```

## Troubleshooting

### Issue: Environment variable not found
```python
# ❌ Throws KeyError if not set
value = os.environ['MY_VAR']

# ✅ Safe with default
value = os.environ.get('MY_VAR', 'default_value')

# ✅ Fail fast with clear error
def get_required_env(key):
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Required environment variable {key} not set")
    return value
```

### Issue: Exceeded size limit
```python
# If environment variables exceed 4KB:
# 1. Move large configs to Parameter Store
# 2. Use S3 for very large configs
# 3. Hardcode non-sensitive defaults

def lambda_handler(event, context):
    # Load large config from S3
    s3 = boto3.client('s3')
    config_bucket = os.environ['CONFIG_BUCKET']
    
    response = s3.get_object(
        Bucket=config_bucket,
        Key='config.json'
    )
    config = json.loads(response['Body'].read())
```

## Complete Example

```yaml
# SAM Template
Resources:
  # Secrets in Secrets Manager
  DatabaseSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      GenerateSecretString:
        SecretStringTemplate: '{"username": "admin"}'
        GenerateStringKey: password
  
  # Configuration in Parameter Store
  ApiConfig:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /myapp/api/config
      Type: String
      Value: '{"endpoint": "https://api.example.com", "timeout": 30}'
  
  # Lambda Function
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          # Non-sensitive configuration
          TABLE_NAME: !Ref MyTable
          LOG_LEVEL: INFO
          STAGE: !Ref Environment
          
          # References to secrets/parameters
          DB_SECRET_ARN: !Ref DatabaseSecret
          API_CONFIG_PATH: /myapp/api/config
      
      Policies:
        # Grant access to secrets and parameters
        - AWSSecretsManagerGetSecretValuePolicy:
            SecretArn: !Ref DatabaseSecret
        - SSMParameterReadPolicy:
            ParameterName: /myapp/api/*
```

## Checklist

- [ ] Never store secrets in plain text
- [ ] Use Secrets Manager for sensitive data
- [ ] Use Parameter Store for configuration
- [ ] Separate configuration by environment
- [ ] Enable encryption for sensitive variables
- [ ] Set appropriate IAM permissions
- [ ] Cache secrets to reduce API calls
- [ ] Rotate secrets regularly
- [ ] Document all environment variables
- [ ] Test with different configurations

## Related Documentation
- AWS Secrets Manager
- Systems Manager Parameter Store
- Lambda Security Best Practices
- KMS Encryption

