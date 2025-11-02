---
category: technical
subcategory: integration
service: lambda
difficulty: advanced
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html
---

# Lambda VPC Connectivity Issues

## Overview
Lambda functions in a VPC can access private resources but may experience connectivity issues. This guide helps diagnose and resolve VPC-related problems.

## Common Issues

### 1. Can't Access Internet
**Symptom**: Lambda in VPC can't reach external APIs or services

**Cause**: No route to internet gateway

**Solutions**:
- Add NAT Gateway to private subnets
- Use VPC endpoints for AWS services
- Move to public subnet (not recommended for security)

### 2. Timeout Accessing AWS Services
**Symptom**: Calls to S3, DynamoDB timeout

**Solution**: Use VPC Endpoints
```yaml
Resources:
  S3Endpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref VPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.s3'
      RouteTableIds:
        - !Ref PrivateRouteTable
```

### 3. Increased Cold Start Time
**Cause**: ENI creation takes 5-15 seconds

**Solutions**:
- Use Provisioned Concurrency
- Enable Hyperplane ENIs (automatic in most regions)
- Minimize VPC if not needed

## VPC Configuration Checklist

- [ ] Subnets in multiple AZs
- [ ] NAT Gateway for internet access
- [ ] VPC Endpoints for AWS services
- [ ] Security groups allow outbound traffic
- [ ] Network ACLs configured correctly
- [ ] DNS resolution enabled
- [ ] Sufficient IP addresses in subnets

## Required IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface",
        "ec2:AssignPrivateIpAddresses",
        "ec2:UnassignPrivateIpAddresses"
      ],
      "Resource": "*"
    }
  ]
}
```

## Best Practices

1. **Use VPC only when needed** - accessing private resources
2. **Hyperplane ENIs** - Reduce cold start impact (enabled by default in most regions)
3. **VPC Endpoints** - For AWS services (S3, DynamoDB, etc.)
4. **Sufficient IPs** - Ensure subnet has enough IP addresses
5. **Monitor ENIs** - Track network interface usage

## Testing VPC Connectivity

```python
import socket
import requests

def lambda_handler(event, context):
    results = {}
    
    # Test DNS resolution
    try:
        socket.gethostbyname('www.google.com')
        results['dns'] = 'OK'
    except:
        results['dns'] = 'FAILED'
    
    # Test internet connectivity
    try:
        response = requests.get('https://www.google.com', timeout=5)
        results['internet'] = 'OK'
    except:
        results['internet'] = 'FAILED'
    
    # Test AWS service (S3)
    try:
        import boto3
        s3 = boto3.client('s3')
        s3.list_buckets()
        results['aws_services'] = 'OK'
    except:
        results['aws_services'] = 'FAILED'
    
    return results
```

## Related Documentation
- VPC Configuration
- NAT Gateway Setup
- VPC Endpoints
- Hyperplane ENIs

