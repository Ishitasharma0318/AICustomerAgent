# 🤖 AI Customer Service Agent

A production-ready, multi-agent AI system for AWS Lambda and API Gateway customer support. This project demonstrates intelligent query routing, three different retrieval strategies (RAG, CAG, and Hybrid), and strategic multi-provider LLM usage.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black)](https://nextjs.org/)

## 🎯 Key Features

- **Multi-Agent System**: Supervisor agent routes queries to specialized workers
- **Three Retrieval Strategies**: Pure RAG, Pure CAG, and Hybrid approaches
- **Cost-Optimized**: AWS Bedrock for routing (~$0.00001), OpenAI for responses
- **Real-Time Streaming**: Server-Sent Events for token-by-token responses
- **Modern Stack**: FastAPI, LangGraph, Next.js, ChromaDB

## 🏗️ Architecture

```
User → Next.js Frontend → FastAPI Backend → LangGraph Orchestrator
                                              ├─ Supervisor (Bedrock)
                                              ├─ Technical Agent (Pure RAG)
                                              ├─ Configuration Agent (Pure CAG)
                                              └─ Billing Agent (Hybrid)
                                                       ↓
                                                  ChromaDB
```

### Specialized Agents

| Agent | Strategy | Purpose | Example Query |
|-------|----------|---------|---------------|
| **Technical** | Pure RAG | Troubleshooting & debugging | "My Lambda function is timing out" |
| **Configuration** | Pure CAG | Best practices & setup | "What are Lambda security best practices?" |
| **Billing** | Hybrid | Pricing & cost optimization | "How much does Lambda cost?" |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- AWS credentials (for Bedrock)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI_Customer_Agent.git
cd AI_Customer_Agent
```

2. **Set up backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env
```

3. **Ingest data into ChromaDB**
```bash
python ingest_data.py
```

4. **Start backend server**
```bash
uvicorn main:app --reload
```

5. **Set up frontend** (new terminal)
```bash
cd frontend
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
```

6. **Open the app**
```
http://localhost:3000
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **LangChain** - LLM orchestration framework
- **LangGraph** - Multi-agent workflow management
- **ChromaDB** - Vector database for document retrieval
- **OpenAI GPT-4** - High-quality response generation
- **AWS Bedrock Claude Haiku** - Cost-effective routing

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful UI components

## 📁 Project Structure

```
AI_Customer_Agent/
├── backend/
│   ├── agents/              # Specialized AI agents
│   │   ├── supervisor.py    # Routes queries (Bedrock)
│   │   ├── technical_agent.py
│   │   ├── configuration_agent.py
│   │   └── billing_agent.py
│   ├── graph/               # LangGraph workflow
│   ├── routers/             # FastAPI endpoints
│   ├── data/                # Knowledge base documents
│   ├── ingest_data.py       # Data ingestion script
│   └── main.py              # FastAPI app
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   └── lib/                 # Utilities
└── docs/                    # Documentation
```



**Technical Support:**
- "My Lambda function is returning a 502 error"
- "What causes cold start issues in Lambda?"

**Configuration:**
- "How do I set up CORS in API Gateway?"
- "What are IAM best practices for Lambda?"

**Billing:**
- "How much does Lambda cost per million requests?"
- "How can I optimize my API Gateway costs?"

## 🔑 Environment Variables

### Backend (.env)
```bash
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=us-east-1
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest

# End-to-end tests
python test_e2e.py

# Agent tests
python test_agents.py
```

## 📊 Performance & Costs

| Component | Latency | Cost per Query |
|-----------|---------|----------------|
| Supervisor Routing | ~150ms | $0.00001 |
| RAG Retrieval | ~50ms | Free (local) |
| Response Generation | ~1-2s | $0.0003 |
| **Total** | **~1.5s** | **~$0.00031** |

## 📚 Documentation

- **Setup Guide**: [`docs/SETUP_GUIDE_FOR_BEGINNERS.md`](docs/SETUP_GUIDE_FOR_BEGINNERS.md)
- **Architecture**: [`docs/ARCHITECTURE_EXPLAINED.md`](docs/ARCHITECTURE_EXPLAINED.md)
- **Sample Queries**: [`docs/sample_queries.json`](docs/sample_queries.json)

## 🎓 Learning Outcomes

This project demonstrates:
- Multi-agent AI architecture with LangGraph
- RAG, CAG, and Hybrid retrieval strategies
- Cost-optimized multi-provider LLM usage
- Real-time streaming with Server-Sent Events
- Modern full-stack development (FastAPI + Next.js)
- Vector database integration with ChromaDB

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome! Feel free to:
- Open an issue for bugs or suggestions
- Fork the repo and submit pull requests
- Star the repo if you find it useful

## 📄 License

MIT License - feel free to use this project for learning or as a foundation for your own work.

## 📧 Contact


Project Link: [https://github.com/yourusername/AI_Customer_Agent](https://github.com/yourusername/AI_Customer_Agent)

