# 🚀 Stage 3 Quick Start: Data Ingestion

Get your vector database up and running in 5 minutes!

---

## Prerequisites

- ✅ Stage 2 completed (environment set up)
- ✅ Python virtual environment activated
- ✅ All dependencies installed from `requirements.txt`

---

## Quick Start (5 Minutes)

### Step 1: Activate Virtual Environment
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Verify Data Files
```bash
# Check that you have documents in all three categories
ls data/technical/      # Should see 10+ .md files
ls data/configuration/  # Should see 8+ .md files
ls data/billing/        # Should see 6+ .md files
```

### Step 3: Run Data Ingestion
```bash
python ingest_data.py
```

**This will:**
- Load all markdown documents from `data/` directory
- Extract metadata from YAML frontmatter
- Split documents into chunks (~1000 chars each)
- Generate embeddings using sentence-transformers
- Store in ChromaDB at `./chroma_db/`

**Expected time:** 30-60 seconds

**Expected output:**
```
======================================================================
AWS CUSTOMER SERVICE AI - DATA INGESTION PIPELINE
======================================================================

Loading 10 documents from 'technical' category...
  ✓ Loaded: lambda-timeout-errors.md
  ✓ Loaded: lambda-memory-errors.md
  [... more files ...]

Chunking 24 documents...
  ✓ Created 87 chunks

Ingesting 87 chunks into ChromaDB...
  ✓ Successfully ingested all documents

======================================================================
✅ Data ingestion completed successfully!
======================================================================
```

### Step 4: Test Retrieval (Optional but Recommended)
```bash
python test_retrieval.py
```

**This will:**
- Test technical support queries
- Test configuration queries
- Test billing queries
- Verify metadata filtering
- Show collection statistics

**Expected time:** 10-20 seconds

---

## Verification

### Check Database Files
```bash
# ChromaDB creates these files
ls -la chroma_db/
# Should see: chroma.sqlite3 and collection directories
```

### Manual Query Test
```python
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

# Test query
results = vector_store.similarity_search(
    "Lambda timeout error",
    k=3
)

for doc in results:
    print(f"File: {doc.metadata['filename']}")
    print(f"Category: {doc.metadata['category']}")
    print(f"Preview: {doc.page_content[:200]}...\n")
```

---

## Common Issues & Solutions

### ❌ Issue: "ModuleNotFoundError: No module named 'chromadb'"
**Solution:**
```bash
# Option 1: Install from requirements
pip install -r requirements.txt

# Option 2: Install directly
pip install chromadb>=0.5.0
```

### ❌ Issue: ChromaDB compilation fails on macOS
**Solution:** See `backend/CHROMADB_INSTALL.md` for detailed workarounds

### ❌ Issue: "No documents found to ingest"
**Solution:**
```bash
# Verify you're in the backend directory
pwd  # Should show: .../backend

# Check data directory exists
ls data/
```

### ❌ Issue: Slow embedding generation
**Solution:**
This is normal on first run. The model downloads once (~80MB):
```
Downloading sentence-transformers model...
This may take 30-60 seconds on first run.
```

Subsequent runs are much faster (2-5 seconds).

---

## What Gets Created

```
backend/
├── chroma_db/                    # ← NEW: Vector database
│   ├── chroma.sqlite3           # SQLite storage
│   └── [collection_uuid]/       # Vector index files
├── ingest_data.py               # ← NEW: Ingestion script
└── test_retrieval.py            # ← NEW: Test script
```

---

## Next Steps

### Option 1: Proceed to Stage 4
Ready to implement the agents!
```bash
# Start implementing agents
# See: docs/STAGE4_QUICKSTART.md (coming soon)
```

### Option 2: Add More Documents
Want to expand the knowledge base?
```bash
# Add new documents to data/ directories
# Follow the template in data/[category]/_template.md

# Re-run ingestion (will replace collection)
python ingest_data.py
```

### Option 3: Experiment with Queries
Try different retrieval strategies:
```python
# Pure RAG for Technical
technical_docs = vector_store.similarity_search(
    query="your question",
    k=5,
    filter={"category": "technical"}
)

# Pure CAG for Configuration (load all at start)
config_docs = vector_store.similarity_search(
    query="",
    k=1000,
    filter={"category": "configuration"}
)

# Hybrid for Billing (first query caches)
billing_docs = vector_store.similarity_search(
    query="pricing question",
    k=10,
    filter={"category": "billing"}
)
```

---

## Understanding the Pipeline

### 1. Document Loading
```
data/technical/lambda-timeout-errors.md
    ↓
[Read file] → [Parse YAML] → [Extract metadata]
```

### 2. Chunking
```
Document (2000 chars)
    ↓
Chunk 1 (chars 0-1000)
Chunk 2 (chars 800-1800)  ← 200 char overlap
Chunk 3 (chars 1600-2000)
```

### 3. Embedding
```
"Lambda functions have a default timeout of 3 seconds..."
    ↓
[sentence-transformers model]
    ↓
[384-dimensional vector: 0.023, -0.134, 0.891, ...]
```

### 4. Storage
```
[Vector + Metadata] → ChromaDB → Persistent Storage
```

### 5. Retrieval
```
Query: "timeout error"
    ↓
[Embed query] → [Similarity search] → [Top K results]
    ↓
Relevant chunks with metadata
```

---

## Performance Expectations

| Metric | Expected Value |
|--------|----------------|
| Initial model download | 30-60 seconds (one time) |
| Document loading | 1-2 seconds |
| Embedding generation | 5-10 seconds (CPU) |
| Database ingestion | 2-5 seconds |
| **Total first run** | **~40-80 seconds** |
| **Subsequent runs** | **~10-20 seconds** |
| Query time | 50-100ms per query |

---

## Tips for Success

### ✅ DO:
- Run ingestion after adding new documents
- Test retrieval after ingestion
- Use metadata filters for category-specific queries
- Check collection statistics to verify ingestion

### ❌ DON'T:
- Don't skip testing retrieval
- Don't modify the vector store manually
- Don't commit `chroma_db/` to Git (it's in `.gitignore`)
- Don't run ingestion while agents are running

---

## Getting Help

### Debug Mode
```bash
# Run with Python warnings enabled
python -W all ingest_data.py

# Verbose ChromaDB logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Collection
```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("aws_docs")
print(f"Total documents: {collection.count()}")
```

---

## Success Criteria

You're ready for Stage 4 when:
- ✅ `chroma_db/` directory exists
- ✅ Ingestion script runs without errors
- ✅ Test script shows 80+ chunks
- ✅ Retrieval returns relevant results
- ✅ All three categories have documents

---

## Time Estimate

- **Setup:** 1 minute
- **First ingestion:** 1-2 minutes
- **Testing:** 1 minute
- **Total:** ~5 minutes

---

🎉 **Congratulations!** Your vector database is ready for the agents!

**Next:** [Stage 4 - Agent Implementation](./STAGE4_QUICKSTART.md)

