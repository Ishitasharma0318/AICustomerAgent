# 🤖 Advanced Customer Service AI for AWS Lambda + API Gateway

A sophisticated, proof-of-concept customer service application powered by a multi-agent AI system. This project demonstrates a modern, scalable architecture for handling diverse customer inquiries about AWS Lambda and API Gateway by routing them to specialized AI agents.

## 🎯 Project Overview

This application showcases:
- **Multi-Agent System**: Hierarchical agent workflow with intelligent query routing
- **Advanced Retrieval Strategies**: RAG, CAG, and Hybrid approaches
- **Multi-Provider LLM Integration**: Strategic use of OpenAI and AWS Bedrock
- **Full-Stack Implementation**: Modern web interface with robust backend API

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│  Frontend   │
│  (Next.js)  │
└──────┬──────┘
       │
       │ HTTP/SSE
       │
┌──────▼──────┐
│   FastAPI   │
│   Backend   │
└──────┬──────┘
       │
       │
┌──────▼──────────────────────────────────────┐
│          LangGraph Orchestrator              │
│  ┌────────────────────────────────────────┐  │
│  │     Supervisor Agent (AWS Bedrock)     │  │
│  │        Routes queries to workers       │  │
│  └─────┬────────────┬──────────┬─────────┘  │
│        │            │          │             │
│  ┌─────▼─────┐ ┌───▼────┐ ┌──▼──────────┐  │
│  │ Technical │ │ Config │ │   Billing   │  │
│  │  Support  │ │ & Best │ │  & Pricing  │  │
│  │   Agent   │ │Practice│ │    Agent    │  │
│  │ (Pure RAG)│ │(PureCAG)│ │(Hybrid R/C)│  │
│  │  OpenAI   │ │ OpenAI │ │   OpenAI    │  │
│  └─────┬─────┘ └───┬────┘ └──┬──────────┘  │
└────────┼───────────┼─────────┼─────────────┘
         │           │         │
         └───────────┴─────────┘
                     │
              ┌──────▼──────┐
              │  ChromaDB   │
              │Vector Store │
              └─────────────┘
```

## 🎪 Three Specialized Agents

### 1. 🔧 Technical Support Agent (Pure RAG)
- **Strategy**: Retrieval-Augmented Generation
- **Purpose**: Troubleshooting, debugging, error resolution
- **Data**: Lambda errors, API Gateway errors, performance issues, CloudWatch debugging
- **Behavior**: Queries vector database for every request to get latest solutions

### 2. ⚙️ Configuration & Best Practices Agent (Pure CAG)
- **Strategy**: Cache-Augmented Generation
- **Purpose**: Best practices, security guidelines, architecture patterns
- **Data**: Lambda/API Gateway best practices, IAM policies, deployment patterns
- **Behavior**: Loads all documentation at startup, no runtime retrieval needed

### 3. 💰 Billing & Pricing Agent (Hybrid RAG/CAG)
- **Strategy**: Hybrid Retrieval + Cache
- **Purpose**: Pricing questions, cost optimization, billing estimates
- **Data**: Lambda/API Gateway pricing, free tier limits, cost optimization strategies
- **Behavior**: First query uses RAG, then caches pricing data for the session

## 🛠️ Technology Stack

### Backend
- **Framework**: Python 3.11+ with FastAPI
- **AI/LLM**: LangChain + LangGraph (LCEL)
- **Vector Database**: ChromaDB (persistent local storage)
- **LLM Providers**:
  - OpenAI GPT-4 (response generation)
  - AWS Bedrock Claude Haiku (cost-effective routing)

### Frontend
- **Framework**: Next.js 14+ with TypeScript
- **UI Library**: shadcn/ui + Tailwind CSS
- **Features**: Real-time streaming responses, conversation history

## 📁 Project Structure

```
AI_Customer_Agent/
├── backend/
│   ├── data/                      # Raw documentation
│   │   ├── technical/            # Technical support docs
│   │   ├── configuration/        # Best practices docs
│   │   └── billing/              # Pricing docs
│   ├── scripts/
│   │   └── scrape_aws_docs.py   # Optional: auto-scrape AWS docs
│   ├── agents/                   # Agent implementations
│   │   ├── supervisor.py         # Routing supervisor
│   │   ├── technical_agent.py    # Pure RAG agent
│   │   ├── configuration_agent.py # Pure CAG agent
│   │   └── billing_agent.py      # Hybrid agent
│   ├── graph/                    # LangGraph workflow
│   │   ├── state.py
│   │   └── workflow.py
│   ├── models/
│   │   └── schemas.py            # Pydantic models
│   ├── routers/
│   │   └── chat.py               # API endpoints
│   ├── ingest_data.py            # Vector DB ingestion
│   ├── main.py                   # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   └── components/
│   │       ├── ChatInterface.tsx
│   │       ├── MessageList.tsx
│   │       └── MessageInput.tsx
│   ├── package.json
│   └── .env.local
├── docs/
│   ├── data_collection_guide.md  # How to gather AWS docs
│   └── sample_queries.json       # Test queries
├── agentic-customer-specs.md     # Project specifications
├── agentic-customer-rubric.md    # Evaluation rubric
└── README.md
```

## 🚀 Development Stages

### ✅ Stage 1: Data Collection & Organization (Current)
Gather and organize AWS Lambda and API Gateway documentation for each specialized agent.

**Status**: 🟢 In Progress

**Deliverables**:
- [ ] Technical support documentation (10-15 docs)
- [ ] Configuration/best practices documentation (8-12 docs)
- [ ] Billing/pricing documentation (6-10 docs)
- [ ] Sample query dataset

### 📋 Stage 2: Environment Setup (Next)
- Set up Python virtual environment
- Install dependencies (FastAPI, LangChain, ChromaDB)
- Initialize Next.js frontend
- Configure API keys

### 📋 Stage 3: Data Ingestion Pipeline
- Build `ingest_data.py` script
- Chunk documents and generate embeddings
- Load into ChromaDB with metadata

### 📋 Stage 4: Worker Agents Implementation
- Implement three specialized agents
- Configure retrieval strategies
- Test agent responses

### 📋 Stage 5: Supervisor Agent & LangGraph
- Build supervisor routing logic
- Implement LangGraph workflow
- Manage conversation state

### 📋 Stage 6: FastAPI Backend
- Create `/chat` endpoint
- Implement streaming responses
- Add error handling

### 📋 Stage 7: Next.js Frontend
- Build chat interface
- Implement streaming display
- Style with Tailwind

### 📋 Stage 8: Testing & Integration
- End-to-end testing
- Bug fixes
- Performance optimization

### 📋 Stage 9: Documentation & Demo
- Comprehensive README
- YouTube demo video (5-10 min)
- Code walkthrough

## 📚 Getting Started (Stage 1)

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key
- AWS account (for Bedrock access)

### Stage 1: Data Collection

1. **Review the data collection guide**:
   ```bash
   cat docs/data_collection_guide.md
   ```

2. **Review sample queries**:
   ```bash
   cat docs/sample_queries.json
   ```

3. **Option A - Manual Collection** (Recommended):
   - Follow the guide in `docs/data_collection_guide.md`
   - Copy AWS documentation sections into markdown files
   - Use templates in `backend/data/*/template.md`

4. **Option B - Automated Scraping**:
   ```bash
   cd backend/scripts
   pip install requests beautifulsoup4 markdownify
   python scrape_aws_docs.py --all
   ```

5. **Organize your data**:
   - `backend/data/technical/` - 10-15 technical docs
   - `backend/data/configuration/` - 8-12 config docs
   - `backend/data/billing/` - 6-10 pricing docs

### What You Need to Provide (Stage 1)

- ⏰ **Time Commitment**: 2-3 hours of focused work
- 📄 **Task**: Collect and organize AWS documentation
- ✅ **Completion**: 24-37 total documents across three categories

## 🎥 Demo Queries

Try these queries to test each agent:

**Technical Support**:
- "My Lambda function is timing out after 3 seconds"
- "What does 502 error mean in API Gateway?"

**Configuration**:
- "What are Lambda security best practices?"
- "How do I configure CORS in API Gateway?"

**Billing**:
- "How much does Lambda cost per million requests?"
- "How can I reduce my API Gateway costs?"

## 📊 Evaluation Criteria

This project will be evaluated on:
- ✅ Multi-agent system implementation (30%)
- ✅ Frontend implementation (20%)
- ✅ System architecture & integration (20%)
- ✅ Data & retrieval strategies (20%)
- ✅ Documentation & demo (10%)

See `agentic-customer-rubric.md` for detailed scoring.

## 🎓 Learning Outcomes

By completing this project, you'll gain hands-on experience with:
- Multi-agent AI systems
- RAG, CAG, and Hybrid retrieval strategies
- LangChain and LangGraph
- Vector databases (ChromaDB)
- FastAPI and async Python
- Next.js and modern React
- Streaming API responses
- Multi-provider LLM integration

## 📝 Development Methodology

This project follows the **Vibe Coding Strategy**: a natural language-driven, iterative approach using AI-assisted development. The developer acts as a "conductor," guiding and validating AI-generated code through conversational prompts.

## 📄 License

This is a portfolio/educational project. Feel free to use it as inspiration for your own projects.

## 🤝 Contributing

This is a solo portfolio project, but feedback and suggestions are welcome!

## 📧 Contact

[Your Name] - [Your Email/LinkedIn]

---

**Current Status**: 📍 Stage 1 - Data Collection Phase

**Last Updated**: November 2, 2024

