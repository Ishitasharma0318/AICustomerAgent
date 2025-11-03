#!/bin/bash

# AWS Temporary Credentials Setup Helper
# This script helps you add your temporary AWS credentials to .env file

echo "========================================================================"
echo "AWS TEMPORARY CREDENTIALS SETUP"
echo "========================================================================"
echo ""
echo "Please get your AWS credentials from:"
echo "1. AWS Console → Top Right → Your Name → 'Security Credentials'"
echo "2. OR AWS Academy → 'AWS Details' → 'Show' under AWS CLI"
echo ""
echo "You need ALL THREE values:"
echo "  - AWS_ACCESS_KEY_ID (starts with ASIA)"
echo "  - AWS_SECRET_ACCESS_KEY (long random string)"
echo "  - AWS_SESSION_TOKEN (very long token starting with IQo...)"
echo ""
echo "========================================================================"
echo ""

# Prompt for credentials
read -p "Enter OPENAI_API_KEY: " OPENAI_KEY
read -p "Enter AWS_ACCESS_KEY_ID (starts with ASIA): " ACCESS_KEY
read -p "Enter AWS_SECRET_ACCESS_KEY: " SECRET_KEY
read -p "Enter AWS_SESSION_TOKEN (very long): " SESSION_TOKEN
read -p "Enter AWS_REGION (default: us-east-1): " REGION

# Set default region if empty
REGION=${REGION:-us-east-1}

# Create .env file
cat > .env << EOF
# ============================================
# API KEYS
# ============================================

# OpenAI Configuration
OPENAI_API_KEY=${OPENAI_KEY}

# AWS Configuration (Temporary Session Credentials)
AWS_ACCESS_KEY_ID=${ACCESS_KEY}
AWS_SECRET_ACCESS_KEY=${SECRET_KEY}
AWS_SESSION_TOKEN=${SESSION_TOKEN}
AWS_REGION=${REGION}

# ============================================
# APPLICATION SETTINGS
# ============================================

# Environment
ENVIRONMENT=development
DEBUG=True

# ChromaDB Settings
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=aws_docs

# FastAPI Settings
API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Model Configuration
SUPERVISOR_MODEL=anthropic.claude-3-haiku-20240307-v1:0
AGENT_MODEL=gpt-4o-mini
EOF

echo ""
echo "========================================================================"
echo "✅ .env file created successfully!"
echo "========================================================================"
echo ""
echo "Testing AWS Bedrock connection..."
echo ""

# Test AWS connection
source venv/bin/activate 2>/dev/null || true
python << PYTEST
import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

try:
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 10,
            'messages': [{'role': 'user', 'content': 'Say: AWS Bedrock connected!'}]
        })
    )
    
    result = json.loads(response['body'].read())
    print('✅ AWS Bedrock connection successful!')
    print(f'   Response: {result["content"][0]["text"]}')
    print('')
    print('⚠️  NOTE: These are temporary credentials.')
    print('   They will expire (usually in 1-12 hours).')
    print('   When they expire, re-run this script with new credentials.')
    
except Exception as e:
    print(f'❌ AWS Bedrock connection failed: {e}')
    print('')
    print('Common issues:')
    print('  - Credentials expired (get new ones)')
    print('  - Model access not enabled in Bedrock console')
    print('  - Wrong region (try us-east-1 or us-west-2)')

PYTEST

echo ""
echo "========================================================================"
echo "SETUP COMPLETE!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "  1. If AWS Bedrock test passed: You're ready for Stage 4!"
echo "  2. If it failed: Check the error messages above"
echo "  3. When credentials expire: Re-run this script"
echo ""

