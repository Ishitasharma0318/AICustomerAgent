# 🏗️ Architecture Explained - Visual Guide

**Understanding how everything connects together**

---

## 📊 The Complete Data Flow

### When a User Asks a Question

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER JOURNEY                                │
└─────────────────────────────────────────────────────────────────────┘

1️⃣  USER TYPES QUESTION
    ↓
    "Why is my Lambda function timing out?"
    ↓
┌───────────────────────────┐
│   FRONTEND (Next.js)      │
│   localhost:3000          │
│                           │
│  • Chat Interface         │
│  • User Input             │
│  • Display Responses      │
└───────────┬───────────────┘
            │
            │ HTTP POST /api/chat
            │ { "message": "Why is my Lambda..." }
            ↓
┌───────────────────────────┐
│   BACKEND (FastAPI)       │
│   localhost:8000          │
│                           │
│  • Receives request       │
│  • Routes to LangGraph    │
└───────────┬───────────────┘
            │
            ↓
┌───────────────────────────────────────────────────────────────────┐
│                    LANGGRAPH WORKFLOW                              │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  STEP 1: SUPERVISOR AGENT                               │    │
│  │  (AWS Bedrock - Claude 3 Haiku)                         │    │
│  │                                                          │    │
│  │  Task: Analyze question & route to correct agent        │    │
│  │  Model: Fast & cheap ($0.00001 per request)             │    │
│  │                                                          │    │
│  │  Analysis:                                               │    │
│  │  "This is about Lambda performance issues"              │    │
│  │  → Route to: TECHNICAL AGENT                            │    │
│  └──────────────────┬──────────────────────────────────────┘    │
│                     │                                             │
│                     ↓                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  STEP 2: TECHNICAL AGENT                                │    │
│  │  (Pure RAG Strategy)                                    │    │
│  │                                                          │    │
│  │  2a) Query ChromaDB                                     │    │
│  │      ↓                                                   │    │
│  │      Search: "Lambda timeout"                           │    │
│  │      ↓                                                   │    │
│  │  ┌─────────────────────────────┐                        │    │
│  │  │      CHROMADB               │                        │    │
│  │  │  (Vector Database)          │                        │    │
│  │  │                             │                        │    │
│  │  │  • Converts query to vector │                        │    │
│  │  │  • Finds similar docs       │                        │    │
│  │  │  • Returns top 5 chunks     │                        │    │
│  │  └──────────┬──────────────────┘                        │    │
│  │             │                                            │    │
│  │             ↓                                            │    │
│  │  Retrieved Documents:                                   │    │
│  │  [1] lambda-timeout-errors.md (relevance: 0.95)        │    │
│  │  [2] lambda-memory-errors.md (relevance: 0.87)         │    │
│  │  [3] cold-start-optimization.md (relevance: 0.82)      │    │
│  │                                                          │    │
│  │  2b) Generate Response with OpenAI                      │    │
│  │      ↓                                                   │    │
│  │  ┌─────────────────────────────┐                        │    │
│  │  │       OPENAI API            │                        │    │
│  │  │   (GPT-4o-mini or GPT-4)    │                        │    │
│  │  │                             │                        │    │
│  │  │  Prompt:                    │                        │    │
│  │  │  "Using these docs:         │                        │    │
│  │  │   [doc content...]          │                        │    │
│  │  │                             │                        │    │
│  │  │   Answer:                   │                        │    │
│  │  │   Why is my Lambda timing   │                        │    │
│  │  │   out?"                     │                        │    │
│  │  └──────────┬──────────────────┘                        │    │
│  │             │                                            │    │
│  │             ↓                                            │    │
│  │  Generated Response:                                    │    │
│  │  "Lambda timeout errors occur when your function        │    │
│  │   exceeds the configured timeout limit. Common causes   │    │
│  │   include: 1) Inefficient code, 2) Slow external APIs..." │   │
│  └─────────────────┬───────────────────────────────────────┘    │
└────────────────────┼───────────────────────────────────────────┘
                     │
                     ↓
            ┌────────────────┐
            │  RESPONSE JSON │
            └────────┬───────┘
                     │
                     ↓
┌───────────────────────────┐
│   BACKEND (FastAPI)       │
│  • Formats response       │
│  • Adds metadata          │
└───────────┬───────────────┘
            │
            │ HTTP Response
            │ { "response": "Lambda timeout errors..." }
            ↓
┌───────────────────────────┐
│   FRONTEND (Next.js)      │
│  • Receives response      │
│  • Displays in chat       │
│  • Shows to user          │
└───────────────────────────┘
            ↓
    USER SEES ANSWER! 🎉
```

---

## 🔄 The Three Retrieval Strategies

### 1️⃣ Pure RAG (Technical Agent)

**Use Case:** Dynamic knowledge base, frequent updates, troubleshooting

```
Every Query:
┌──────────────┐
│ User Query   │
└──────┬───────┘
       ↓
┌──────────────┐
│  ChromaDB    │  ← Search EVERY time
│  Retrieval   │
└──────┬───────┘
       ↓
┌──────────────┐
│  Generate    │
│  Response    │
└──────────────┘

Pros: Always fresh, handles new questions
Cons: Slower (~100ms per query)
Cost: Medium
```

**Example Flow:**
```python
# User asks: "Lambda timeout error"

# 1. Retrieve from ChromaDB
docs = vector_store.similarity_search(
    query="Lambda timeout error",
    k=5,
    filter={"category": "technical"}
)

# 2. Generate response with OpenAI
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a technical support agent."},
        {"role": "user", "content": f"Context: {docs}\n\nQuestion: Lambda timeout error"}
    ]
)
```

### 2️⃣ Pure CAG (Configuration Agent)

**Use Case:** Static knowledge, policies, best practices, documentation

```
Session Start (Once):
┌──────────────┐
│ Load ALL     │
│ Config Docs  │  ← Load once per session
└──────┬───────┘
       ↓
┌──────────────┐
│ Cache in     │
│ Memory       │
└──────┬───────┘
       ↓
Every Query:
┌──────────────┐
│ Search       │
│ Cache        │  ← Fast! No DB query
└──────┬───────┘
       ↓
┌──────────────┐
│ Generate     │
│ Response     │
└──────────────┘

Pros: Super fast (~10ms), no DB overhead
Cons: Uses more memory, not for large datasets
Cost: Low
```

**Example Flow:**
```python
# Session start: Load all config docs once
session_cache = vector_store.similarity_search(
    query="",  # Empty query returns all
    k=1000,
    filter={"category": "configuration"}
)

# User asks: "Lambda best practices"
# Search in-memory cache (fast!)
relevant_docs = search_in_memory(session_cache, "Lambda best practices")

# Generate response
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a configuration expert."},
        {"role": "user", "content": f"Context: {relevant_docs}\n\nQuestion: ..."}
    ]
)
```

### 3️⃣ Hybrid RAG/CAG (Billing Agent)

**Use Case:** Semi-static data that's frequently accessed together

```
First Query per Session:
┌──────────────┐
│ User Query   │
└──────┬───────┘
       ↓
┌──────────────┐
│  ChromaDB    │  ← Retrieve from DB
│  Retrieval   │
└──────┬───────┘
       ↓
┌──────────────┐
│ Cache        │  ← Save results
│ Results      │
└──────┬───────┘
       ↓
┌──────────────┐
│ Generate     │
│ Response     │
└──────────────┘

Subsequent Queries:
┌──────────────┐
│ User Query   │
└──────┬───────┘
       ↓
┌──────────────┐
│ Search       │  ← Use cached data
│ Cache        │
└──────┬───────┘
       ↓
┌──────────────┐
│ Generate     │
│ Response     │
└──────────────┘

Pros: Fast after first query, fresh data
Cons: Complex to implement
Cost: Low-Medium
```

**Example Flow:**
```python
# First query: "Lambda pricing"
if "billing" not in session_cache:
    # RAG: Retrieve from ChromaDB
    docs = vector_store.similarity_search(
        query="Lambda pricing",
        k=10,
        filter={"category": "billing"}
    )
    # Cache for session
    session_cache["billing"] = docs
else:
    # CAG: Use cached docs
    docs = session_cache["billing"]

# Generate response
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...]
)
```

---

## 🔑 Why Two LLM Providers?

### AWS Bedrock (Routing) vs OpenAI (Responses)

```
┌──────────────────────────────────────────────────────────────┐
│                    COST OPTIMIZATION                         │
└──────────────────────────────────────────────────────────────┘

AWS BEDROCK (Claude 3 Haiku)
├─ Task: Quick routing decisions
├─ Cost: ~$0.00025 per 1K tokens
├─ Speed: ~200ms response time
├─ When: Every request (determines agent)
└─ Example: "Is this technical? → Yes"

OPENAI (GPT-4o-mini)
├─ Task: Detailed, helpful responses
├─ Cost: ~$0.15 per 1M tokens (input)
├─ Speed: ~1-2s response time
├─ When: Only after routing
└─ Example: "Here's how to fix Lambda timeouts..."

💰 SAVINGS EXAMPLE:
┌────────────────────────┬─────────┬──────────┐
│ Scenario               │ Bedrock │ OpenAI   │
├────────────────────────┼─────────┼──────────┤
│ 100 routing decisions  │ $0.003  │ $0.15    │
│ 100 full responses     │ $0.15   │ $0.15    │
├────────────────────────┼─────────┼──────────┤
│ TOTAL for 100 queries  │ $0.153  │ $0.30    │
├────────────────────────┼─────────┼──────────┤
│ SAVINGS                │         │ 49%!     │
└────────────────────────┴─────────┴──────────┘
```

---

## 💾 ChromaDB Deep Dive

### What Actually Happens Inside ChromaDB

```
┌──────────────────────────────────────────────────────────────┐
│                     DOCUMENT INGESTION                        │
└──────────────────────────────────────────────────────────────┘

1. Raw Document:
   ┌────────────────────────────────────────────┐
   │ # Lambda Timeout Errors                    │
   │                                            │
   │ Lambda functions have a default timeout    │
   │ of 3 seconds but can be configured up      │
   │ to 15 minutes (900 seconds)...             │
   │                                            │
   │ [2000 characters total]                    │
   └────────────────────────────────────────────┘
                    ↓
2. Text Splitting:
   ┌────────────────────────────────────────────┐
   │ Chunk 1 (chars 0-1000):                    │
   │ "Lambda functions have a default..."       │
   └────────────────────────────────────────────┘
   ┌────────────────────────────────────────────┐
   │ Chunk 2 (chars 800-1800):                  │
   │ "...timeout of 3 seconds. To increase..."  │
   │ (200 char overlap with Chunk 1)            │
   └────────────────────────────────────────────┘
                    ↓
3. Embedding Generation:
   ┌────────────────────────────────────────────┐
   │ Text: "Lambda functions have a default..." │
   │         ↓ (sentence-transformers)          │
   │ Vector: [0.023, -0.134, 0.891, ..., 0.445] │
   │         (384 dimensions)                    │
   └────────────────────────────────────────────┘
                    ↓
4. Store in ChromaDB:
   ┌────────────────────────────────────────────┐
   │ Vector Index (HNSW)                        │
   │ ├─ Vector: [0.023, -0.134, ...]           │
   │ ├─ Metadata: {                             │
   │ │    category: "technical",                │
   │ │    service: "lambda",                    │
   │ │    filename: "lambda-timeout-errors.md"  │
   │ │  }                                        │
   │ └─ Content: "Lambda functions have a..."   │
   └────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     QUERY & RETRIEVAL                         │
└──────────────────────────────────────────────────────────────┘

1. User Query:
   ┌────────────────────────────────────────────┐
   │ "Why is my Lambda slow?"                   │
   └────────────────────────────────────────────┘
                    ↓
2. Convert to Vector:
   ┌────────────────────────────────────────────┐
   │ Query: "Why is my Lambda slow?"            │
   │         ↓ (same embedding model)           │
   │ Vector: [0.019, -0.128, 0.883, ..., 0.438] │
   └────────────────────────────────────────────┘
                    ↓
3. Similarity Search:
   ┌────────────────────────────────────────────┐
   │ Calculate Cosine Similarity:               │
   │                                            │
   │ Query vector vs All stored vectors         │
   │                                            │
   │ Doc 1: similarity = 0.95 ✓ (timeout doc)  │
   │ Doc 2: similarity = 0.87 ✓ (memory doc)   │
   │ Doc 3: similarity = 0.82 ✓ (cold start)   │
   │ Doc 4: similarity = 0.45 ✗ (not relevant) │
   └────────────────────────────────────────────┘
                    ↓
4. Return Top K:
   ┌────────────────────────────────────────────┐
   │ Top 3 Most Similar Documents:              │
   │                                            │
   │ 1. lambda-timeout-errors.md (0.95)        │
   │    "Lambda functions timeout when..."      │
   │                                            │
   │ 2. lambda-memory-errors.md (0.87)         │
   │    "Memory issues can cause slow..."       │
   │                                            │
   │ 3. cold-start-optimization.md (0.82)      │
   │    "Cold starts add latency..."            │
   └────────────────────────────────────────────┘
```

### ChromaDB Storage Structure

```
backend/chroma_db/
├── chroma.sqlite3                    # Metadata database
│   ├── Collections                   # Table
│   ├── Documents                     # Table
│   └── Embeddings                    # References
│
└── [collection-uuid]/                # Vector data
    ├── data_level0.bin              # HNSW index layer 0
    ├── index_metadata.pickle        # Index configuration
    ├── header.bin                   # Collection metadata
    └── link_lists.bin               # HNSW graph structure
```

---

## 🎯 Complete Request Example

Let's trace a real request through the entire system:

```
USER ASKS: "How much does Lambda cost?"

┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Frontend → Backend                                  │
└─────────────────────────────────────────────────────────────┘
POST http://localhost:8000/api/chat
{
  "message": "How much does Lambda cost?",
  "session_id": "abc123"
}

┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Supervisor Agent (AWS Bedrock)                      │
└─────────────────────────────────────────────────────────────┘
Bedrock API Call:
{
  "model": "anthropic.claude-3-haiku",
  "messages": [{
    "role": "system",
    "content": "You are a routing agent. Analyze the query and return: technical, configuration, or billing"
  }, {
    "role": "user",
    "content": "How much does Lambda cost?"
  }]
}

Bedrock Response:
{
  "decision": "billing",
  "confidence": "high",
  "reasoning": "Question about pricing"
}

Cost: $0.00001
Time: 150ms

┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Billing Agent - ChromaDB Retrieval                  │
└─────────────────────────────────────────────────────────────┘
ChromaDB Query:
{
  "query": "How much does Lambda cost?",
  "k": 5,
  "filter": {"category": "billing"}
}

ChromaDB Process:
1. Convert query to vector [0.234, -0.891, ...]
2. Search billing documents
3. Calculate similarities:
   - lambda-pricing-details.md: 0.94
   - free-tier-limits.md: 0.88
   - cost-optimization.md: 0.82

ChromaDB Returns:
[
  {
    "content": "AWS Lambda pricing is based on requests and duration. The free tier includes 1M requests per month and 400,000 GB-seconds...",
    "metadata": {
      "filename": "lambda-pricing-details.md",
      "category": "billing"
    }
  },
  {...},
  {...}
]

Time: 50ms

┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Generate Response (OpenAI)                          │
└─────────────────────────────────────────────────────────────┘
OpenAI API Call:
{
  "model": "gpt-4o-mini",
  "messages": [{
    "role": "system",
    "content": "You are a billing expert. Use the provided context to answer questions."
  }, {
    "role": "user",
    "content": "Context: [ChromaDB results]\n\nQuestion: How much does Lambda cost?"
  }]
}

OpenAI Response:
{
  "response": "AWS Lambda pricing consists of two components:\n\n1. **Requests**: $0.20 per 1 million requests\n2. **Duration**: $0.0000166667 per GB-second\n\n**Free Tier** (every month):\n- 1 million free requests\n- 400,000 GB-seconds of compute time\n\n**Example**: If your function...[detailed explanation]"
}

Cost: $0.0003 (300 tokens)
Time: 1.2s

┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Backend → Frontend                                  │
└─────────────────────────────────────────────────────────────┘
Response:
{
  "response": "AWS Lambda pricing consists of...",
  "agent_used": "billing",
  "sources": ["lambda-pricing-details.md"],
  "timestamp": "2025-11-03T10:30:00Z"
}

┌─────────────────────────────────────────────────────────────┐
│ TOTAL TIME & COST                                           │
└─────────────────────────────────────────────────────────────┘
Total Time: ~1.4 seconds
Total Cost: $0.00031
Breakdown:
  - Bedrock routing: $0.00001 (3%)
  - ChromaDB: $0 (free)
  - OpenAI response: $0.0003 (97%)
```

---

## 🎉 Summary

### Key Takeaways

1. **ChromaDB** = Your smart document storage (local, free)
2. **AWS Bedrock** = Your cheap router ($0.00001 per decision)
3. **OpenAI** = Your quality responder ($0.0003 per answer)
4. **Three strategies** = Optimize for different use cases

### Total Cost per Conversation
- Routing: $0.00001
- Response: $0.0003
- **Total: ~$0.0003 per question answered** 🎯

### Setup Time
- Get API keys: 10 minutes
- Configure .env: 2 minutes
- Run ingestion: 2 minutes
- **Total: ~15 minutes** ⏱️

---

**Ready to start?** → See `docs/SETUP_GUIDE_FOR_BEGINNERS.md`

