"""
Test script for Stage 4 - Agent Implementation
Tests all three specialized agents and supervisor routing
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.supervisor import SupervisorAgent
from agents.technical_agent import TechnicalSupportAgent
from agents.configuration_agent import ConfigurationAgent
from agents.billing_agent import BillingAgent
from langchain_core.messages import HumanMessage


async def test_supervisor_routing():
    """Test supervisor agent routing capabilities"""
    print("\n" + "="*80)
    print("TESTING SUPERVISOR ROUTING")
    print("="*80)
    
    supervisor = SupervisorAgent()
    
    test_queries = [
        ("My Lambda function is timing out", "technical"),
        ("What are Lambda best practices?", "configuration"),
        ("How much does Lambda cost?", "billing"),
        ("I'm getting a 502 error from API Gateway", "technical"),
        ("How do I configure CORS?", "configuration"),
        ("What's included in the free tier?", "billing"),
    ]
    
    for query, expected_agent in test_queries:
        print(f"\n📝 Query: {query}")
        result = await supervisor.route_query(query, [])
        actual_agent = result["next_agent"]
        confidence = result["confidence"]
        method = result["routing_method"]
        
        status = "✅" if actual_agent == expected_agent else "❌"
        print(f"{status} Routed to: {actual_agent} (expected: {expected_agent})")
        print(f"   Confidence: {confidence} | Method: {method}")
        print(f"   Reasoning: {result['reasoning']}")


async def test_technical_agent():
    """Test technical support agent (Pure RAG)"""
    print("\n" + "="*80)
    print("TESTING TECHNICAL SUPPORT AGENT (Pure RAG)")
    print("="*80)
    
    try:
        agent = TechnicalSupportAgent()
        
        test_query = "My Lambda function is timing out after 3 seconds. How do I fix it?"
        print(f"\n📝 Query: {test_query}")
        
        result = await agent.process(
            message=test_query,
            history=[HumanMessage(content=test_query)],
            session_id="test_session_1"
        )
        
        print(f"\n✅ Agent Type: {result.get('agent_type', 'N/A')}")
        print(f"✅ Retrieval Count: {result.get('retrieval_count', 0)}")
        print(f"✅ Sources: {len(result.get('sources', []))}")
        print(f"\n📄 Response:\n{result['response'][:500]}...")
        print(f"\n📚 Source Files:")
        for i, source in enumerate(result.get('sources', [])[:3], 1):
            print(f"   {i}. {source.get('filename', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Error testing technical agent: {e}")
        import traceback
        traceback.print_exc()


async def test_configuration_agent():
    """Test configuration agent (Pure CAG)"""
    print("\n" + "="*80)
    print("TESTING CONFIGURATION AGENT (Pure CAG)")
    print("="*80)
    
    try:
        agent = ConfigurationAgent()
        
        test_query = "What are the security best practices for Lambda functions?"
        print(f"\n📝 Query: {test_query}")
        
        result = await agent.process(
            message=test_query,
            history=[HumanMessage(content=test_query)],
            session_id="test_session_2"
        )
        
        print(f"\n✅ Agent Type: {result.get('agent_type', 'N/A')}")
        print(f"✅ Cache Used: {result.get('cache_used', False)}")
        print(f"✅ Cached Doc Count: {result.get('cached_doc_count', 0)}")
        print(f"✅ Sources: {len(result.get('sources', []))}")
        print(f"\n📄 Response:\n{result['response'][:500]}...")
        print(f"\n📚 Source Files:")
        for i, source in enumerate(result.get('sources', [])[:3], 1):
            print(f"   {i}. {source.get('filename', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Error testing configuration agent: {e}")
        import traceback
        traceback.print_exc()


async def test_billing_agent():
    """Test billing agent (Hybrid RAG/CAG)"""
    print("\n" + "="*80)
    print("TESTING BILLING AGENT (Hybrid RAG/CAG)")
    print("="*80)
    
    try:
        agent = BillingAgent()
        
        # First query - should use RAG
        query1 = "How much does Lambda cost per request?"
        print(f"\n📝 First Query (RAG mode): {query1}")
        
        result1 = await agent.process(
            message=query1,
            history=[HumanMessage(content=query1)],
            session_id="test_session_3"
        )
        
        print(f"\n✅ Agent Type: {result1.get('agent_type', 'N/A')}")
        print(f"✅ Retrieval Mode: {result1.get('retrieval_mode', 'N/A')}")
        print(f"✅ Cache Created: {result1.get('cache_created', False)}")
        print(f"✅ Retrieval Count: {result1.get('retrieval_count', 0)}")
        print(f"\n📄 Response:\n{result1['response'][:500]}...")
        
        # Second query - should use CAG (cached)
        query2 = "What about the free tier for Lambda?"
        print(f"\n\n📝 Second Query (CAG mode): {query2}")
        
        result2 = await agent.process(
            message=query2,
            history=[HumanMessage(content=query2)],
            session_id="test_session_3"  # Same session
        )
        
        print(f"\n✅ Agent Type: {result2.get('agent_type', 'N/A')}")
        print(f"✅ Retrieval Mode: {result2.get('retrieval_mode', 'N/A')}")
        print(f"✅ Cache Used: {result2.get('cache_used', False)}")
        print(f"✅ Cached Doc Count: {result2.get('cached_doc_count', 0)}")
        print(f"\n📄 Response:\n{result2['response'][:500]}...")
        
    except Exception as e:
        print(f"❌ Error testing billing agent: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("STAGE 4 AGENT TESTING SUITE")
    print("="*80)
    print("\nThis script tests all implemented agents:")
    print("- Supervisor Agent (AWS Bedrock routing)")
    print("- Technical Support Agent (Pure RAG)")
    print("- Configuration Agent (Pure CAG)")
    print("- Billing Agent (Hybrid RAG/CAG)")
    print("\n" + "="*80)
    
    # Check if vector database exists
    chroma_path = Path(__file__).parent / "chroma_db"
    if not chroma_path.exists():
        print("\n⚠️  WARNING: ChromaDB not found at ./chroma_db")
        print("⚠️  Please run 'python ingest_data.py' first to populate the vector database")
        print("\n❌ Skipping agent tests (requires vector database)")
        return
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  WARNING: OPENAI_API_KEY not set in environment")
        print("⚠️  Worker agents require OpenAI API key for GPT-4")
        print("\n❌ Skipping agent tests")
        return
    
    # Run tests
    await test_supervisor_routing()
    await test_technical_agent()
    await test_configuration_agent()
    await test_billing_agent()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
    print("\nNext steps:")
    print("1. Review test results above")
    print("2. Verify routing is working correctly")
    print("3. Check that each agent uses the correct retrieval strategy")
    print("4. Test the full workflow with LangGraph")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())

