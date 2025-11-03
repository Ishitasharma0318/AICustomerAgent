# 🎓 Complete Setup Guide for Beginners

**Everything you need to know to get your AI Customer Service Agent running!**

---

## 📚 Table of Contents
1. [Understanding the Architecture](#understanding-the-architecture)
2. [What is ChromaDB?](#what-is-chromadb)
3. [Setting Up OpenAI](#setting-up-openai)
4. [Setting Up AWS Bedrock](#setting-up-aws-bedrock)
5. [Connecting Everything Together](#connecting-everything-together)
6. [Step-by-Step Setup](#step-by-step-setup)
7. [Testing Your Setup](#testing-your-setup)

---

## 🏗️ Understanding the Architecture

### The Big Picture

Think of your application like a restaurant with specialized chefs:

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION                         │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │   Frontend   │◄────►│   Backend    │                   │
│  │  (Next.js)   │      │  (FastAPI)   │                   │
│  └──────────────┘      └──────┬───────┘                   │
│                               │                             │
│                    ┌──────────┴──────────┐                 │
│                    │                     │                  │
│              ┌─────▼──────┐      ┌──────▼─────┐           │
│              │ Supervisor │      │  ChromaDB  │           │
│              │   Agent    │      │ (Knowledge │           │
│              │ (Router)   │      │   Base)    │           │
│              └─────┬──────┘      └────────────┘           │
│                    │                                        │
│         ┌──────────┼──────────┐                           │
│         │          │          │                            │
│    ┌────▼───┐ ┌───▼────┐ ┌──▼─────┐                      │
│    │Technical│ │Config  │ │Billing │                      │
│    │ Agent  │ │ Agent  │ │ Agent  │                      │
│    └────────┘ └────────┘ └────────┘                      │
└─────────────────────────────────────────────────────────────┘
           │                              │
    ┌──────▼────────┐            ┌───────▼────────┐
    │  AWS Bedrock  │            │     OpenAI     │
    │  (Routing)    │            │  (Responses)   │
    │  Fast & Cheap │            │ High Quality   │
    └───────────────┘            └────────────────┘
```

### What Each Component Does

**1. Frontend (Next.js)**
- The chat interface users see
- Sends user messages to backend
- Displays AI responses

**2. Backend (FastAPI)**
- Receives user queries
- Orchestrates the AI agents
- Returns responses to frontend

**3. ChromaDB**
- Stores your AWS documentation
- Retrieves relevant info when agents need it
- Works like a smart search engine

**4. AWS Bedrock**
- Analyzes user questions (cheap & fast)
- Decides which agent to use
- Think of it as the "receptionist"

**5. OpenAI**
- Generates detailed, helpful responses
- Handles the actual conversation
- Think of it as the "expert consultant"

---

## 💾 What is ChromaDB?

### Simple Explanation

**ChromaDB is like a smart filing cabinet for your documents.**

#### Traditional Search (Bad)
```
User asks: "Why is my Lambda slow?"
Computer searches for: "Lambda" AND "slow"
Returns: Every document with those words (not very helpful!)
```

#### Vector Search with ChromaDB (Good!)
```
User asks: "Why is my Lambda slow?"
ChromaDB understands meaning:
  → Returns docs about: cold starts, timeouts, memory issues
  → Ranked by relevance (most helpful first!)
```

### How ChromaDB Works in This Project

#### Step 1: Setup (One Time)
```
Your AWS docs (.md files)
    ↓
Ingest script reads them
    ↓
Converts text to "vectors" (numerical representations)
    ↓
Stores in ChromaDB database
```

#### Step 2: When User Asks Question
```
User: "My Lambda function times out"
    ↓
Convert question to vector
    ↓
ChromaDB finds similar vectors (similar meaning)
    ↓
Returns relevant documentation chunks
    ↓
Agent uses these chunks to answer
```

### What You Need to Know

✅ **ChromaDB runs locally on your computer**
- No external service needed
- No API keys required
- Completely free

✅ **ChromaDB stores data in a folder**
- Location: `backend/chroma_db/`
- Automatically created when you run ingestion
- Can delete and recreate anytime

✅ **One-time setup required**
- Run `python ingest_data.py` once
- Only re-run if you add new documents
- Takes ~1 minute

---

## 🔑 Setting Up OpenAI

### What You Need

**OpenAI API Key** - Used to generate high-quality responses

### Step-by-Step Instructions

#### 1. Create OpenAI Account
1. Go to https://platform.openai.com/signup
2. Sign up with your email
3. Verify your email address

#### 2. Get API Key
1. Log in to https://platform.openai.com
2. Click your profile icon (top right)
3. Select "View API keys" or go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Give it a name like "AI Customer Agent"
6. **COPY THE KEY IMMEDIATELY** (you won't see it again!)

**Your key looks like:**
```
sk-proj-abc123def456ghi789...
```

#### 3. Add Credits (If Needed)
- New accounts get $5 free credit
- If expired, add payment method at https://platform.openai.com/account/billing
- Minimum: $5
- This project will use ~$0.10-0.50 per day of testing

#### 4. Important Notes
⚠️ **NEVER share your API key**
⚠️ **NEVER commit it to Git**
✅ Store it in `.env` file (automatically ignored by Git)

---

## ☁️ Setting Up AWS Bedrock

### What You Need

**AWS Account with Bedrock Access** - Used for fast, cheap routing decisions

### Step-by-Step Instructions

#### 1. Create AWS Account (if you don't have one)
1. Go to https://aws.amazon.com
2. Click "Create an AWS Account"
3. Follow the signup process
4. **You'll need a credit card** (but free tier is generous)

#### 2. Enable AWS Bedrock
1. Log in to AWS Console: https://console.aws.amazon.com
2. Search for "Bedrock" in the top search bar
3. Click "Amazon Bedrock"
4. **Important:** Check your region (top right)
   - Recommended: `us-east-1` (N. Virginia)
   - Or: `us-west-2` (Oregon)
5. Click "Get started" if prompted
6. Click "Model access" in left sidebar
7. Click "Edit" or "Manage model access"
8. Enable these models:
   - ✅ **Claude 3 Haiku** (by Anthropic) - Fast & cheap routing
   - ✅ **Claude 3.5 Sonnet** (by Anthropic) - Optional, better quality
   - Or: ✅ **Amazon Nova Lite/Micro** - AWS's own models
9. Click "Request model access" or "Save changes"
10. Wait 2-5 minutes for approval (usually instant)

#### 3. Create IAM User & Access Keys

**Why?** Your application needs credentials to access AWS Bedrock.

**Steps:**

1. Go to IAM Console: https://console.aws.amazon.com/iam
2. Click "Users" in left sidebar
3. Click "Create user"
4. Username: `ai-customer-agent`
5. Click "Next"
6. **Attach permissions:**
   - Click "Attach policies directly"
   - Search and select: `AmazonBedrockFullAccess`
   - (Or create custom policy with just bedrock:InvokeModel)
7. Click "Next" → "Create user"

8. **Create Access Key:**
   - Click on the user you just created
   - Go to "Security credentials" tab
   - Scroll to "Access keys" section
   - Click "Create access key"
   - Select "Application running outside AWS"
   - Click "Next" → "Create access key"
   - **COPY BOTH:**
     - Access key ID: `AKIA...`
     - Secret access key: `abc123...`
   - Click "Done"

#### 4. Important Notes
⚠️ **NEVER share your AWS credentials**
⚠️ **NEVER commit them to Git**
✅ Store them in `.env` file
✅ Use IAM user (not root account) for security

---

## 🔗 Connecting Everything Together

### The .env File - Your Configuration Center

All your API keys and settings go in **ONE FILE**: `backend/.env`

This file is:
- ✅ Automatically ignored by Git (safe!)
- ✅ Read by your application at startup
- ✅ Easy to update without touching code

### Creating Your .env File

```bash
# Navigate to backend directory
cd backend

# Copy the example file
cp .env.example .env

# Now edit .env with your keys
```

---

## 🚀 Step-by-Step Setup

### Complete Setup Process (20 minutes)

#### Step 1: Clone & Install (5 min)

```bash
# Navigate to your project
cd AI_Customer_Agent/backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify dependencies installed
pip list | grep -E "langchain|chromadb|openai|boto3"
```

#### Step 2: Configure .env File (5 min)

Create `backend/.env` file with your credentials:

```bash
# ============================================
# API KEYS - ADD YOUR REAL KEYS HERE
# ============================================

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# AWS Configuration
AWS_ACCESS_KEY_ID=AKIA_YOUR_ACTUAL_KEY_HERE
AWS_SECRET_ACCESS_KEY=your_actual_secret_key_here
AWS_REGION=us-east-1

# ============================================
# APPLICATION SETTINGS (Keep as is)
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
```

**Replace:**
- `YOUR_ACTUAL_KEY_HERE` with your OpenAI key
- `AKIA_YOUR_ACTUAL_KEY_HERE` with your AWS Access Key ID
- `your_actual_secret_key_here` with your AWS Secret Key

#### Step 3: Ingest Documents to ChromaDB (2 min)

```bash
# Make sure you're in backend/ directory
cd backend

# Run ingestion script
python ingest_data.py
```

**What happens:**
```
1. Loads all .md files from data/ folders
2. Splits them into chunks
3. Converts to vectors (embeddings)
4. Stores in chroma_db/ folder
```

**Expected output:**
```
======================================================================
AWS CUSTOMER SERVICE AI - DATA INGESTION PIPELINE
======================================================================
Loading documents...
✓ Technical: 10 docs
✓ Configuration: 8 docs  
✓ Billing: 6 docs
✓ Created 87 chunks
✓ Successfully ingested all documents
======================================================================
✅ Data ingestion completed successfully!
======================================================================
```

#### Step 4: Test ChromaDB Connection (1 min)

```bash
python test_retrieval.py
```

**Should see:**
```
✅ ALL RETRIEVAL TESTS PASSED!
```

#### Step 5: Test API Keys (5 min)

Create `backend/test_connections.py`:

```python
"""Test script to verify all API connections"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("TESTING API CONNECTIONS")
print("=" * 70)

# Test 1: Check .env loaded
print("\n[1/4] Checking environment variables...")
openai_key = os.getenv("OPENAI_API_KEY")
aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

if openai_key and openai_key.startswith("sk-"):
    print("  ✓ OpenAI API key found")
else:
    print("  ✗ OpenAI API key missing or invalid")

if aws_key and aws_key.startswith("AKIA"):
    print("  ✓ AWS Access Key found")
else:
    print("  ✗ AWS Access Key missing or invalid")

if aws_secret and len(aws_secret) > 20:
    print("  ✓ AWS Secret Key found")
else:
    print("  ✗ AWS Secret Key missing or invalid")

print(f"  ✓ AWS Region: {aws_region}")

# Test 2: Test OpenAI connection
print("\n[2/4] Testing OpenAI connection...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5
    )
    print(f"  ✓ OpenAI connected! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"  ✗ OpenAI error: {str(e)}")

# Test 3: Test AWS Bedrock connection
print("\n[3/4] Testing AWS Bedrock connection...")
try:
    import boto3
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=aws_region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )
    
    # Test with a simple request
    import json
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Say 'test'"}]
        })
    )
    
    result = json.loads(response['body'].read())
    print(f"  ✓ AWS Bedrock connected! Response: {result['content'][0]['text']}")
except Exception as e:
    print(f"  ✗ AWS Bedrock error: {str(e)}")
    print("    Common issues:")
    print("    - Model access not enabled in Bedrock console")
    print("    - Wrong region (try us-east-1 or us-west-2)")
    print("    - IAM permissions missing")

# Test 4: Test ChromaDB
print("\n[4/4] Testing ChromaDB connection...")
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vector_store = Chroma(
        collection_name="aws_docs",
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    results = vector_store.similarity_search("test", k=1)
    print(f"  ✓ ChromaDB connected! Documents: {vector_store._collection.count()}")
except Exception as e:
    print(f"  ✗ ChromaDB error: {str(e)}")
    print("    Run: python ingest_data.py")

print("\n" + "=" * 70)
print("CONNECTION TEST COMPLETE")
print("=" * 70)
```

Run it:
```bash
python test_connections.py
```

**Expected output:**
```
======================================================================
TESTING API CONNECTIONS
======================================================================

[1/4] Checking environment variables...
  ✓ OpenAI API key found
  ✓ AWS Access Key found
  ✓ AWS Secret Key found
  ✓ AWS Region: us-east-1

[2/4] Testing OpenAI connection...
  ✓ OpenAI connected! Response: test

[3/4] Testing AWS Bedrock connection...
  ✓ AWS Bedrock connected! Response: test

[4/4] Testing ChromaDB connection...
  ✓ ChromaDB connected! Documents: 87

======================================================================
✅ CONNECTION TEST COMPLETE
======================================================================
```

#### Step 6: Start Backend Server (1 min)

```bash
cd backend
python main.py
```

**Should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Keep this terminal open!

#### Step 7: Start Frontend (1 min)

Open a **NEW terminal**:

```bash
cd frontend
npm run dev
```

**Should see:**
```
  ▲ Next.js 16.0.1
  - Local:        http://localhost:3000
```

#### Step 8: Test the Full Application

1. Open browser: http://localhost:3000
2. You should see the chat interface
3. Try asking: "Why is my Lambda function timing out?"
4. The AI should respond with helpful information!

---

## 🧪 Testing Your Setup

### Quick Tests

#### Test 1: ChromaDB
```bash
cd backend
python -c "
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vs = Chroma(collection_name='aws_docs', persist_directory='./chroma_db', embedding_function=embeddings)
print(f'Documents: {vs._collection.count()}')
"
```

#### Test 2: OpenAI
```bash
python -c "
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
r = client.chat.completions.create(model='gpt-3.5-turbo', messages=[{'role':'user','content':'Hi'}], max_tokens=5)
print(f'OpenAI: {r.choices[0].message.content}')
"
```

#### Test 3: AWS Bedrock
```bash
python -c "
import os, json, boto3
from dotenv import load_dotenv
load_dotenv()
bedrock = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION'))
r = bedrock.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body=json.dumps({'anthropic_version':'bedrock-2023-05-31','max_tokens':10,'messages':[{'role':'user','content':'Hi'}]})
)
print(f'Bedrock: {json.loads(r[\"body\"].read())[\"content\"][0][\"text\"]}')
"
```

---

## 🐛 Troubleshooting Common Issues

### Issue 1: "OpenAI API key not found"
**Solution:**
```bash
# Check if .env file exists
ls -la backend/.env

# Check if key is set
cat backend/.env | grep OPENAI_API_KEY

# If missing, add it:
echo "OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE" >> backend/.env
```

### Issue 2: "AWS credentials not found"
**Solution:**
```bash
# Verify AWS credentials in .env
cat backend/.env | grep AWS_

# Should see:
# AWS_ACCESS_KEY_ID=AKIA...
# AWS_SECRET_ACCESS_KEY=...
# AWS_REGION=us-east-1
```

### Issue 3: "Bedrock model access denied"
**Solutions:**
1. Go to AWS Bedrock console
2. Click "Model access" (left sidebar)
3. Enable Claude 3 Haiku
4. Wait 2-5 minutes for approval
5. Verify region matches your .env (us-east-1)

### Issue 4: "ChromaDB collection not found"
**Solution:**
```bash
cd backend
python ingest_data.py  # Run ingestion
```

### Issue 5: "No space left on device" (ChromaDB)
**Solution:**
- See `backend/CHROMADB_INSTALL.md`
- Try: `pip install chromadb --no-build-isolation`
- Or use Docker: `docker run -p 8000:8000 chromadb/chroma`

---

## 💰 Cost Estimates

### OpenAI Costs
- **Testing (1 hour)**: ~$0.01-0.05
- **Development (1 day)**: ~$0.50-2.00
- **Per conversation**: ~$0.001-0.01

Using GPT-3.5-Turbo or GPT-4o-mini (cheapest options)

### AWS Bedrock Costs
- **Testing**: Essentially $0 (fractions of a cent)
- **Per routing decision**: ~$0.0001
- **Much cheaper than OpenAI** (that's why we use it for routing!)

### ChromaDB Costs
- **FREE!** (runs locally, no API calls)

### Total Estimated Costs
- **Setup & Testing**: $0.50-1.00
- **Per day of development**: $1-5
- **Per production conversation**: $0.001-0.02

---

## 🎉 You're Ready!

### Checklist

- [ ] OpenAI API key configured
- [ ] AWS Bedrock access enabled
- [ ] AWS credentials configured
- [ ] ChromaDB ingestion completed
- [ ] All connection tests passing
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Can chat with the AI!

### What's Next?

- **Stage 4**: Implement the specialized agents
- **Stage 5**: Connect frontend to backend
- **Stage 6**: Add streaming responses
- **Stage 7**: Deploy to production

---

## 📞 Need Help?

### Useful Commands
```bash
# Check if services are running
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Restart backend
cd backend && python main.py

# Restart frontend
cd frontend && npm run dev

# Re-ingest documents
cd backend && python ingest_data.py

# View logs
tail -f backend/logs/*.log  # If logging enabled
```

### Quick Reference

| Component | Location | Check |
|-----------|----------|-------|
| OpenAI Key | backend/.env | `OPENAI_API_KEY=sk-...` |
| AWS Keys | backend/.env | `AWS_ACCESS_KEY_ID=AKIA...` |
| ChromaDB | backend/chroma_db/ | Folder exists with files |
| Backend | http://localhost:8000 | `/health` endpoint |
| Frontend | http://localhost:3000 | Chat interface loads |

---

**Created**: November 3, 2025  
**Updated**: November 3, 2025  
**Status**: Complete beginner-friendly setup guide

