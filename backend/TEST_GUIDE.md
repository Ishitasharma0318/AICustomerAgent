# Test Execution Guide

Quick reference for running tests on the AI Customer Agent system.

## 🚀 Quick Start

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

# Run comprehensive E2E tests
python test_e2e.py
```

## 📋 Available Test Suites

### 1. Comprehensive End-to-End Tests
**File**: `test_e2e.py`  
**Purpose**: Tests all system components in one go

```bash
# Full test suite
python test_e2e.py

# Quick mode (skip slower tests)
python test_e2e.py --quick

# Verbose output
python test_e2e.py --verbose
```

**What it tests**:
- ✅ Environment & API connections
- ✅ Vector database retrieval
- ✅ All 4 agents (supervisor + workers)
- ✅ API endpoints
- ✅ Workflow integration
- ✅ Frontend checklist

**Duration**: ~2-3 minutes

---

### 2. Connection Tests
**File**: `test_connections.py`  
**Purpose**: Verify API connections

```bash
python test_connections.py
```

**What it tests**:
- OpenAI API connection
- AWS Bedrock connection
- ChromaDB connection
- Environment variables

**Duration**: ~30 seconds

---

### 3. Agent Tests
**File**: `test_agents.py`  
**Purpose**: Test individual agent functionality

```bash
python test_agents.py
```

**What it tests**:
- Supervisor routing
- Technical agent (Pure RAG)
- Configuration agent (Pure CAG)
- Billing agent (Hybrid RAG/CAG)

**Duration**: ~1-2 minutes

---

### 4. API Integration Tests
**File**: `test_api.py`  
**Purpose**: Test FastAPI endpoints

```bash
# Make sure API server is running first
python main.py &

# Then run tests
python test_api.py
```

**What it tests**:
- Health check endpoint
- Root endpoint
- Chat endpoint
- Session management
- Streaming endpoint

**Duration**: ~1 minute

---

### 5. Retrieval Tests
**File**: `test_retrieval.py`  
**Purpose**: Test vector database queries

```bash
python test_retrieval.py
```

**What it tests**:
- Technical document retrieval
- Configuration document retrieval
- Billing document retrieval
- Metadata filtering

**Duration**: ~10 seconds

---

## 🎯 Running Specific Test Categories

### Test Vector Database Only
```bash
python -c "
from test_e2e import test_vector_database_retrieval
import asyncio
asyncio.run(test_vector_database_retrieval())
"
```

### Test Agents Only
```bash
python -c "
from test_e2e import test_individual_agents
import asyncio
asyncio.run(test_individual_agents())
"
```

### Test Workflow Only
```bash
python -c "
from test_e2e import test_workflow_integration
import asyncio
asyncio.run(test_workflow_integration())
"
```

---

## 🔍 Interpreting Test Results

### Success Indicators
- ✅ Green checkmark: Test passed
- 🟢 Green text: Successful operation
- Numbers in green: Good metrics

### Warning Indicators
- ⚠️ Yellow warning: Non-critical issue
- 🟡 Yellow text: Needs attention
- Partial pass: Some tests passed

### Error Indicators
- ❌ Red X: Test failed
- 🔴 Red text: Error occurred
- Error messages: Details provided

---

## 📊 Test Results

### Where Results Are Stored
- **Terminal output**: Real-time progress
- **JSON file**: `test_results_stage7.json`
- **Reports**: `STAGE7_COMPLETE.md` and `STAGE7_STATUS.md`

### Reading JSON Results
```bash
# View test results
cat test_results_stage7.json | python -m json.tool

# Get summary
cat test_results_stage7.json | jq '.summary'
```

---

## 🛠️ Troubleshooting

### Test Fails: "Cannot connect to API"
**Solution**: Start the API server first
```bash
python main.py &
```

### Test Fails: "ChromaDB not found"
**Solution**: Ingest documents first
```bash
python ingest_data.py
```

### Test Fails: "OpenAI API error"
**Solution**: Check API key in `.env`
```bash
grep OPENAI_API_KEY .env
```

### Test Fails: "AWS Bedrock error"
**Solution**: Check AWS credentials
```bash
grep AWS_ .env
```

---

## ⚙️ Test Configuration

### Environment Variables Required
```bash
# In .env file
OPENAI_API_KEY=sk-...
AWS_ACCESS_KEY_ID=ASIA...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=...      # For temporary credentials
AWS_REGION=us-east-1
```

### Test Timeouts
- Connection tests: 10 seconds
- API tests: 60 seconds
- Agent tests: 120 seconds
- E2E tests: 180 seconds

---

## 📈 Performance Benchmarks

### Expected Performance
| Test Category | Duration | Status |
|--------------|----------|--------|
| Vector Retrieval | 2-3s | Fast |
| Individual Agents | 60-90s | Normal |
| Workflow | 40-60s | Normal |
| API Integration | 20-40s | Normal |
| Total E2E | 150-200s | Normal |

### If Tests Are Slow
- Check internet connection
- Verify OpenAI API is responding
- Check AWS region latency
- Monitor system resources

---

## 🎓 Best Practices

### Before Running Tests
1. ✅ Ensure virtual environment is activated
2. ✅ Check that ChromaDB is populated
3. ✅ Verify environment variables are set
4. ✅ Start API server (for API tests)

### During Test Execution
1. 📝 Watch for warnings (non-critical)
2. 📊 Note performance metrics
3. 🐛 Check error messages carefully
4. ⏱️ Monitor test duration

### After Test Completion
1. 📄 Review test report
2. 📊 Check pass rate
3. 🔍 Investigate failures
4. 📝 Document any issues

---

## 🚨 Common Issues

### Issue: "Model not found"
**Cause**: Test script uses old model ID  
**Impact**: None (system still works)  
**Fix**: Update model ID in test script

### Issue: "Session token expired"
**Cause**: AWS temporary credentials expired  
**Impact**: AWS tests fail  
**Fix**: Refresh AWS credentials

### Issue: "Rate limit exceeded"
**Cause**: Too many API calls  
**Impact**: Tests fail  
**Fix**: Wait and retry

---

## 📚 Additional Resources

- **Full Report**: `../STAGE7_COMPLETE.md`
- **Quick Status**: `../STAGE7_STATUS.md`
- **Setup Guide**: `../docs/SETUP_GUIDE_FOR_BEGINNERS.md`
- **Architecture**: `../docs/ARCHITECTURE_EXPLAINED.md`

---

## 🎯 Quick Commands Reference

```bash
# Comprehensive testing
python test_e2e.py

# Individual test suites
python test_connections.py
python test_agents.py
python test_api.py
python test_retrieval.py

# Start API server
python main.py

# View test results
cat test_results_stage7.json

# Check system status
python test_connections.py

# Run quick validation
python test_e2e.py --quick
```

---

**Last Updated**: November 3, 2025  
**Test Suite Version**: 1.0.0  
**System Status**: 🟢 All tests passing

