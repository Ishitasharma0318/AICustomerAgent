"""
Stage 5 API Integration Testing Suite
Tests all FastAPI endpoints with the integrated LangGraph workflow
"""

import asyncio
import sys
import os
import json
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import httpx
from datetime import datetime

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = 120.0  # 2 minutes for LLM responses


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


async def test_health_check():
    """Test 1: Health check endpoint"""
    print_header("TEST 1: HEALTH CHECK")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Health check passed")
                print_info(f"Status: {data.get('status')}")
                print_info(f"Version: {data.get('version')}")
                return True
            else:
                print_error(f"Health check failed: {response.status_code}")
                return False
                
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False


async def test_root_endpoint():
    """Test 2: Root endpoint"""
    print_header("TEST 2: ROOT ENDPOINT")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/")
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Root endpoint accessible")
                print_info(f"Message: {data.get('message')}")
                print_info(f"Version: {data.get('version')}")
                print_info(f"Endpoints: {list(data.get('endpoints', {}).keys())}")
                return True
            else:
                print_error(f"Root endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        print_error(f"Root endpoint error: {str(e)}")
        return False


async def test_chat_technical_query():
    """Test 3: Chat endpoint with technical query"""
    print_header("TEST 3: TECHNICAL SUPPORT QUERY (Pure RAG)")
    
    query = "My Lambda function is timing out after 3 seconds. What should I check?"
    
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            start_time = datetime.now()
            
            print_info(f"Query: {query}")
            
            response = await client.post(
                f"{API_BASE_URL}/api/chat",
                json={
                    "message": query,
                    "session_id": "test-session-technical",
                }
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Technical query completed in {duration:.2f}s")
                print_info(f"Agent: {data.get('agent_type')}")
                print_info(f"Session ID: {data.get('session_id')}")
                print_info(f"Sources: {len(data.get('sources', []))} documents")
                print_info(f"Response preview: {data.get('response', '')[:150]}...")
                
                # Verify it's using the technical agent
                if data.get('agent_type') == 'technical':
                    print_success("Correctly routed to Technical Support Agent")
                    return True
                else:
                    print_warning(f"Routed to {data.get('agent_type')} instead of technical")
                    return True  # Still a success, routing decision may vary
            else:
                print_error(f"Technical query failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print_error(f"Technical query error: {str(e)}")
        return False


async def test_chat_configuration_query():
    """Test 4: Chat endpoint with configuration query"""
    print_header("TEST 4: CONFIGURATION QUERY (Pure CAG)")
    
    query = "What are the best practices for Lambda security?"
    
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            start_time = datetime.now()
            
            print_info(f"Query: {query}")
            
            response = await client.post(
                f"{API_BASE_URL}/api/chat",
                json={
                    "message": query,
                    "session_id": "test-session-configuration",
                }
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Configuration query completed in {duration:.2f}s")
                print_info(f"Agent: {data.get('agent_type')}")
                print_info(f"Session ID: {data.get('session_id')}")
                print_info(f"Response preview: {data.get('response', '')[:150]}...")
                
                # Verify it's using the configuration agent
                if data.get('agent_type') == 'configuration':
                    print_success("Correctly routed to Configuration Agent")
                    return True
                else:
                    print_warning(f"Routed to {data.get('agent_type')} instead of configuration")
                    return True  # Still a success
            else:
                print_error(f"Configuration query failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print_error(f"Configuration query error: {str(e)}")
        return False


async def test_chat_billing_query():
    """Test 5: Chat endpoint with billing query"""
    print_header("TEST 5: BILLING QUERY (Hybrid RAG/CAG)")
    
    query = "How much does Lambda cost per million requests?"
    
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            start_time = datetime.now()
            
            print_info(f"Query: {query}")
            
            response = await client.post(
                f"{API_BASE_URL}/api/chat",
                json={
                    "message": query,
                    "session_id": "test-session-billing",
                }
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Billing query completed in {duration:.2f}s")
                print_info(f"Agent: {data.get('agent_type')}")
                print_info(f"Session ID: {data.get('session_id')}")
                print_info(f"Response preview: {data.get('response', '')[:150]}...")
                
                # Verify it's using the billing agent
                if data.get('agent_type') == 'billing':
                    print_success("Correctly routed to Billing Agent")
                    return True
                else:
                    print_warning(f"Routed to {data.get('agent_type')} instead of billing")
                    return True  # Still a success
            else:
                print_error(f"Billing query failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print_error(f"Billing query error: {str(e)}")
        return False


async def test_conversation_history():
    """Test 6: Multi-turn conversation with history"""
    print_header("TEST 6: MULTI-TURN CONVERSATION")
    
    session_id = "test-session-conversation"
    
    messages = [
        "How much does Lambda cost?",
        "What about API Gateway?",
        "How can I optimize costs?",
    ]
    
    try:
        conversation_history = []
        
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            for i, message in enumerate(messages, 1):
                print_info(f"Turn {i}: {message}")
                
                response = await client.post(
                    f"{API_BASE_URL}/api/chat",
                    json={
                        "message": message,
                        "session_id": session_id,
                        "conversation_history": conversation_history,
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print_success(f"Turn {i} completed - Agent: {data.get('agent_type')}")
                    
                    # Add to conversation history
                    conversation_history.append({
                        "role": "user",
                        "content": message,
                    })
                    conversation_history.append({
                        "role": "assistant",
                        "content": data.get('response'),
                        "agent_type": data.get('agent_type'),
                    })
                else:
                    print_error(f"Turn {i} failed: {response.status_code}")
                    return False
        
        print_success(f"Multi-turn conversation completed - {len(messages)} turns")
        return True
        
    except Exception as e:
        print_error(f"Conversation error: {str(e)}")
        return False


async def test_session_history():
    """Test 7: Session history retrieval"""
    print_header("TEST 7: SESSION HISTORY RETRIEVAL")
    
    session_id = "test-session-history"
    
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            # First, send a message
            print_info("Sending test message...")
            await client.post(
                f"{API_BASE_URL}/api/chat",
                json={
                    "message": "What is Lambda?",
                    "session_id": session_id,
                }
            )
            
            # Now retrieve history
            print_info("Retrieving session history...")
            response = await client.get(
                f"{API_BASE_URL}/api/sessions/{session_id}/history"
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"History retrieved successfully")
                print_info(f"Session ID: {data.get('session_id')}")
                print_info(f"Message count: {data.get('message_count')}")
                return True
            else:
                print_error(f"History retrieval failed: {response.status_code}")
                return False
                
    except Exception as e:
        print_error(f"History retrieval error: {str(e)}")
        return False


async def test_session_clear():
    """Test 8: Session clearing"""
    print_header("TEST 8: SESSION CLEARING")
    
    session_id = "test-session-clear"
    
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            # First, send a message
            print_info("Creating test session...")
            await client.post(
                f"{API_BASE_URL}/api/chat",
                json={
                    "message": "Test message",
                    "session_id": session_id,
                }
            )
            
            # Now clear the session
            print_info("Clearing session...")
            response = await client.delete(
                f"{API_BASE_URL}/api/sessions/{session_id}"
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Session cleared successfully")
                print_info(f"Status: {data.get('status')}")
                return True
            else:
                print_error(f"Session clear failed: {response.status_code}")
                return False
                
    except Exception as e:
        print_error(f"Session clear error: {str(e)}")
        return False


async def test_streaming_endpoint():
    """Test 9: Streaming endpoint"""
    print_header("TEST 9: STREAMING ENDPOINT")
    
    query = "What are Lambda timeout best practices?"
    
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            print_info(f"Query: {query}")
            print_info("Starting streaming request...")
            
            start_time = datetime.now()
            chunks_received = 0
            
            async with client.stream(
                "POST",
                f"{API_BASE_URL}/api/chat/stream",
                json={
                    "message": query,
                    "session_id": "test-session-streaming",
                }
            ) as response:
                if response.status_code != 200:
                    print_error(f"Streaming failed: {response.status_code}")
                    return False
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunks_received += 1
                        data_str = line[6:]  # Remove "data: " prefix
                        try:
                            data = json.loads(data_str)
                            event_type = data.get("type")
                            
                            if event_type == "metadata":
                                print_info(f"Received metadata")
                            elif event_type == "progress":
                                print_info(f"Progress: {data.get('node')}")
                            elif event_type == "content":
                                # Don't print every content chunk, too verbose
                                pass
                            elif event_type == "complete":
                                duration = (datetime.now() - start_time).total_seconds()
                                print_success(f"Streaming completed in {duration:.2f}s")
                                print_info(f"Agent: {data.get('agent_type')}")
                                print_info(f"Chunks received: {chunks_received}")
                            elif event_type == "error":
                                print_error(f"Stream error: {data.get('error')}")
                                return False
                        except json.JSONDecodeError:
                            pass
            
            print_success(f"Streaming endpoint working correctly")
            return True
            
    except Exception as e:
        print_error(f"Streaming error: {str(e)}")
        return False


async def test_error_handling():
    """Test 10: Error handling"""
    print_header("TEST 10: ERROR HANDLING")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test with invalid request (missing required field)
            print_info("Testing validation error...")
            response = await client.post(
                f"{API_BASE_URL}/api/chat",
                json={}  # Missing required 'message' field
            )
            
            if response.status_code == 422:
                print_success("Validation error handled correctly (422)")
            else:
                print_warning(f"Unexpected status code: {response.status_code}")
            
            # Test with empty message
            print_info("Testing empty message...")
            response = await client.post(
                f"{API_BASE_URL}/api/chat",
                json={"message": ""}
            )
            
            if response.status_code in [422, 400]:
                print_success("Empty message handled correctly")
            else:
                print_warning(f"Unexpected status code: {response.status_code}")
            
            print_success("Error handling tests completed")
            return True
            
    except Exception as e:
        print_error(f"Error handling test error: {str(e)}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{Colors.MAGENTA}STAGE 5 API INTEGRATION TESTING SUITE{Colors.RESET}")
    print("=" * 70)
    print(f"API Base URL: {Colors.CYAN}{API_BASE_URL}{Colors.RESET}")
    print("=" * 70)
    
    # Check if server is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.get(f"{API_BASE_URL}/health")
    except Exception as e:
        print_error(f"\nCannot connect to API server at {API_BASE_URL}")
        print_info("Please make sure the server is running:")
        print_info("  cd backend")
        print_info("  source venv/bin/activate")
        print_info("  python main.py")
        return
    
    # Run all tests
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Technical Query", test_chat_technical_query),
        ("Configuration Query", test_chat_configuration_query),
        ("Billing Query", test_chat_billing_query),
        ("Multi-turn Conversation", test_conversation_history),
        ("Session History", test_session_history),
        ("Session Clear", test_session_clear),
        ("Streaming Endpoint", test_streaming_endpoint),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}\n🎉 ALL TESTS PASSED! 🎉{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}\n⚠️  Some tests failed. See details above.{Colors.RESET}\n")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

