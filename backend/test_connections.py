"""
Test script to verify all API connections (OpenAI, AWS Bedrock, ChromaDB)
Run this after setting up your .env file to ensure everything is configured correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def print_step(step_num, total_steps, description):
    """Print a formatted step"""
    print(f"\n[{step_num}/{total_steps}] {description}")

def test_environment_variables():
    """Test if environment variables are loaded"""
    print_step(1, 4, "Checking environment variables...")
    
    all_good = True
    
    # Check OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key.startswith("sk-"):
        print("  ✓ OpenAI API key found")
    else:
        print("  ✗ OpenAI API key missing or invalid")
        print("    Expected format: sk-proj-...")
        all_good = False
    
    # Check AWS Access Key
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    if aws_key and aws_key.startswith("AKIA"):
        print("  ✓ AWS Access Key found")
    else:
        print("  ✗ AWS Access Key missing or invalid")
        print("    Expected format: AKIA...")
        all_good = False
    
    # Check AWS Secret Key
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if aws_secret and len(aws_secret) > 20:
        print("  ✓ AWS Secret Key found")
    else:
        print("  ✗ AWS Secret Key missing or invalid")
        all_good = False
    
    # Check AWS Region
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    print(f"  ✓ AWS Region: {aws_region}")
    
    return all_good, openai_key, aws_key, aws_secret, aws_region

def test_openai_connection(api_key):
    """Test connection to OpenAI API"""
    print_step(2, 4, "Testing OpenAI connection...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Connection successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"  ✓ OpenAI connected successfully!")
        print(f"  ✓ Test response: {result}")
        return True
        
    except Exception as e:
        print(f"  ✗ OpenAI connection failed: {str(e)}")
        print("\n  Common issues:")
        print("    - Invalid API key")
        print("    - Insufficient credits (check https://platform.openai.com/account/billing)")
        print("    - Network connectivity issues")
        return False

def test_bedrock_connection(aws_key, aws_secret, aws_region):
    """Test connection to AWS Bedrock"""
    print_step(3, 4, "Testing AWS Bedrock connection...")
    
    try:
        import boto3
        import json
        
        # Create Bedrock client
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret
        )
        
        # Test with Claude 3 Haiku
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [
                    {"role": "user", "content": "Say 'Connection successful'"}
                ]
            })
        )
        
        result = json.loads(response['body'].read())
        response_text = result['content'][0]['text']
        print(f"  ✓ AWS Bedrock connected successfully!")
        print(f"  ✓ Test response: {response_text}")
        print(f"  ✓ Model: Claude 3 Haiku")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"  ✗ AWS Bedrock connection failed: {error_msg}")
        print("\n  Common issues:")
        
        if "could not be found" in error_msg.lower() or "accessdenied" in error_msg.lower():
            print("    - Model access not enabled in Bedrock console")
            print("    - Go to: https://console.aws.amazon.com/bedrock")
            print("    - Click 'Model access' → Enable 'Claude 3 Haiku'")
            print("    - Wait 2-5 minutes for approval")
        
        if "region" in error_msg.lower():
            print(f"    - Current region: {aws_region}")
            print("    - Try regions: us-east-1 or us-west-2")
            print("    - Update AWS_REGION in .env file")
        
        if "credential" in error_msg.lower() or "signature" in error_msg.lower():
            print("    - Invalid AWS credentials")
            print("    - Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        
        if "permission" in error_msg.lower():
            print("    - IAM user lacks Bedrock permissions")
            print("    - Attach 'AmazonBedrockFullAccess' policy to IAM user")
        
        return False

def test_chromadb_connection():
    """Test connection to ChromaDB"""
    print_step(4, 4, "Testing ChromaDB connection...")
    
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load vector store
        vector_store = Chroma(
            collection_name="aws_docs",
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        
        # Get document count
        doc_count = vector_store._collection.count()
        
        if doc_count > 0:
            print(f"  ✓ ChromaDB connected successfully!")
            print(f"  ✓ Total documents: {doc_count}")
            
            # Test a query
            results = vector_store.similarity_search("Lambda timeout", k=1)
            if results:
                print(f"  ✓ Query test successful")
                print(f"  ✓ Sample doc: {results[0].metadata.get('filename', 'Unknown')}")
            
            return True
        else:
            print(f"  ⚠️  ChromaDB connected but no documents found")
            print("  → Run: python ingest_data.py")
            return False
        
    except Exception as e:
        error_msg = str(e)
        print(f"  ✗ ChromaDB connection failed: {error_msg}")
        print("\n  Common issues:")
        
        if "No such file or directory" in error_msg or "does not exist" in error_msg:
            print("    - ChromaDB not initialized")
            print("    - Run: python ingest_data.py")
        
        if "Collection" in error_msg and "does not exist" in error_msg:
            print("    - Collection 'aws_docs' not found")
            print("    - Run: python ingest_data.py")
        
        return False

def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    env_vars, openai, bedrock, chroma = results
    
    print("\n✅ Passed:")
    if env_vars:
        print("  • Environment variables configured")
    if openai:
        print("  • OpenAI API connection")
    if bedrock:
        print("  • AWS Bedrock connection")
    if chroma:
        print("  • ChromaDB connection")
    
    failed = []
    if not env_vars:
        failed.append("Environment variables")
    if not openai:
        failed.append("OpenAI API")
    if not bedrock:
        failed.append("AWS Bedrock")
    if not chroma:
        failed.append("ChromaDB")
    
    if failed:
        print("\n❌ Failed:")
        for item in failed:
            print(f"  • {item}")
    
    print("\n" + "=" * 70)
    
    if all(results):
        print("🎉 ALL TESTS PASSED! Your setup is complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Start backend: python main.py")
        print("  2. Start frontend: cd ../frontend && npm run dev")
        print("  3. Open browser: http://localhost:3000")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED. Please fix the issues above.")
        print("=" * 70)
        print("\nFor help, see: docs/SETUP_GUIDE_FOR_BEGINNERS.md")
        return 1

def main():
    """Main test execution"""
    print_header("API CONNECTION TEST SUITE")
    print("\nThis script verifies your setup for:")
    print("  • OpenAI API (for generating responses)")
    print("  • AWS Bedrock (for routing decisions)")
    print("  • ChromaDB (for document retrieval)")
    
    # Test 1: Environment variables
    env_result, openai_key, aws_key, aws_secret, aws_region = test_environment_variables()
    
    # Test 2: OpenAI (only if env vars are good)
    openai_result = False
    if env_result and openai_key:
        openai_result = test_openai_connection(openai_key)
    else:
        print_step(2, 4, "Testing OpenAI connection...")
        print("  ⏭️  Skipped (environment variables not configured)")
    
    # Test 3: AWS Bedrock (only if env vars are good)
    bedrock_result = False
    if env_result and aws_key and aws_secret:
        bedrock_result = test_bedrock_connection(aws_key, aws_secret, aws_region)
    else:
        print_step(3, 4, "Testing AWS Bedrock connection...")
        print("  ⏭️  Skipped (AWS credentials not configured)")
    
    # Test 4: ChromaDB (always test)
    chroma_result = test_chromadb_connection()
    
    # Print summary
    results = (env_result, openai_result, bedrock_result, chroma_result)
    exit_code = print_summary(results)
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

