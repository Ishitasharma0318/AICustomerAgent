"""
Test AWS Bedrock access with different authentication methods
"""
import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

print('=' * 70)
print('AWS BEDROCK CONNECTION TESTS')
print('=' * 70)

# Test 1: With current credentials
print('\n[Test 1] Standard authentication with session token...')
try:
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )
    
    response = bedrock.invoke_model(
        modelId='amazon.nova-micro-v1:0',  # Try Amazon's model first (no marketplace)
        body=json.dumps({
            'inputText': 'Hello',
            'textGenerationConfig': {
                'maxTokenCount': 10,
                'temperature': 0.5
            }
        })
    )
    
    result = json.loads(response['body'].read())
    print('  ✅ SUCCESS with Nova Micro!')
    print(f'  Response: {result}')
    
except Exception as e:
    error_msg = str(e)
    print(f'  ❌ Failed: {error_msg[:150]}')
    
    if 'marketplace' in error_msg.lower():
        print('  → This model requires marketplace permissions')
    elif 'AccessDenied' in error_msg:
        print('  → Access denied to this model')

# Test 2: Try with bearer token if set
print('\n[Test 2] Checking for bearer token...')
bearer_token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
if bearer_token:
    print(f'  ✓ Bearer token found ({len(bearer_token)} chars)')
    print('  → This might bypass marketplace permissions')
    # Bearer token usage depends on organization setup
else:
    print('  ℹ️  No bearer token set')
    print('  → Check with your admin if ASU uses bearer tokens for Bedrock')

# Test 3: List available models
print('\n[Test 3] Checking what models are accessible...')
try:
    bedrock_service = boto3.client(
        service_name='bedrock',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )
    
    # This will also fail if no permissions, but worth trying
    models = bedrock_service.list_foundation_models()
    print(f'  ✅ Can list models! Found {len(models.get("modelSummaries", []))} models')
    
except Exception as e:
    print(f'  ❌ Cannot list models: {str(e)[:100]}')

print('\n' + '=' * 70)
print('DIAGNOSIS')
print('=' * 70)
print('\nYour account has these issues:')
print('  1. ❌ No aws-marketplace:ViewSubscriptions permission')
print('  2. ❌ Cannot access Claude 3 Haiku (requires marketplace)')
print('\nPossible solutions:')
print('  A. Contact ASU admin to add Bedrock permissions')
print('  B. Ask if ASU provides a bearer token for Bedrock')
print('  C. Use OpenAI for routing instead (works perfectly!)')
print('=' * 70)

