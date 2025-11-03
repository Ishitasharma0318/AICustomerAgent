"""
Chat API endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, Dict
import uuid
import json
import logging
from datetime import datetime

from models.schemas import ChatRequest, ChatResponse, AgentType
from graph.workflow import create_workflow
from langchain_core.messages import HumanMessage, AIMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Global workflow instance (initialized once)
_workflow = None
_session_histories: Dict[str, list] = {}


def get_workflow():
    """Get or create the workflow instance"""
    global _workflow
    if _workflow is None:
        logger.info("Initializing LangGraph workflow...")
        _workflow = create_workflow()
        logger.info("Workflow initialized successfully")
    return _workflow


def get_session_history(session_id: str) -> list:
    """Get conversation history for a session"""
    if session_id not in _session_histories:
        _session_histories[session_id] = []
    return _session_histories[session_id]


def add_to_session_history(session_id: str, message: dict):
    """Add a message to session history"""
    if session_id not in _session_histories:
        _session_histories[session_id] = []
    _session_histories[session_id].append(message)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    
    Processes user messages through the multi-agent system and returns responses.
    """
    start_time = datetime.now()
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        logger.info(f"[{session_id}] Received chat request: {request.message[:50]}...")
        
        # Get workflow
        workflow = get_workflow()
        
        # Build message history
        messages = []
        
        # Add conversation history if provided
        if request.conversation_history:
            for msg in request.conversation_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))
        
        # Add current user message
        current_message = HumanMessage(content=request.message)
        messages.append(current_message)
        
        # Initialize state
        initial_state = {
            "messages": messages,
            "next_agent": "supervisor",
            "session_id": session_id,
            "cached_data": None,
            "routing_decision": None,
        }
        
        logger.info(f"[{session_id}] Invoking workflow...")
        
        # Run the workflow
        result = await workflow.ainvoke(initial_state)
        
        # Extract response
        final_messages = result.get("messages", [])
        if not final_messages:
            raise ValueError("No response generated from workflow")
        
        # Get the last message (AI response)
        last_message = final_messages[-1]
        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Determine which agent handled the request
        routing_decision = result.get("routing_decision", {})
        agent_type_str = routing_decision.get("next_agent", "supervisor")
        
        # Map agent string to AgentType enum
        agent_type_map = {
            "technical": AgentType.TECHNICAL,
            "configuration": AgentType.CONFIGURATION,
            "billing": AgentType.BILLING,
            "supervisor": AgentType.SUPERVISOR,
        }
        agent_type = agent_type_map.get(agent_type_str, AgentType.SUPERVISOR)
        
        # Extract sources if available
        sources = routing_decision.get("sources", [])
        
        # Log successful response
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"[{session_id}] Request completed in {duration:.2f}s by {agent_type.value} agent")
        
        # Add to session history
        add_to_session_history(session_id, {
            "role": "user",
            "content": request.message,
            "timestamp": start_time.isoformat(),
        })
        add_to_session_history(session_id, {
            "role": "assistant",
            "content": response_text,
            "agent_type": agent_type.value,
            "timestamp": datetime.now().isoformat(),
        })
        
        return ChatResponse(
            response=response_text,
            agent_type=agent_type,
            session_id=session_id,
            sources=sources,
        )
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"[{session_id}] Request failed after {duration:.2f}s: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint
    
    Returns streaming responses for real-time user experience.
    """
    
    async def generate_response() -> AsyncGenerator[str, None]:
        """Generate streaming response"""
        session_id = None
        start_time = datetime.now()
        
        try:
            # Generate session ID if not provided
            session_id = request.session_id or str(uuid.uuid4())
            
            logger.info(f"[{session_id}] Starting streaming request: {request.message[:50]}...")
            
            # Get workflow
            workflow = get_workflow()
            
            # Build message history
            messages = []
            
            # Add conversation history if provided
            if request.conversation_history:
                for msg in request.conversation_history:
                    if msg.role == "user":
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role == "assistant":
                        messages.append(AIMessage(content=msg.content))
            
            # Add current user message
            current_message = HumanMessage(content=request.message)
            messages.append(current_message)
            
            # Initialize state
            initial_state = {
                "messages": messages,
                "next_agent": "supervisor",
                "session_id": session_id,
                "cached_data": None,
                "routing_decision": None,
            }
            
            # Stream metadata first
            metadata = {
                "type": "metadata",
                "session_id": session_id,
                "timestamp": start_time.isoformat(),
            }
            yield f"data: {json.dumps(metadata)}\n\n"
            
            # Run the workflow with streaming
            logger.info(f"[{session_id}] Starting workflow stream...")
            
            # For now, we'll use astream_events for token-level streaming
            # LangGraph's astream() provides node-level streaming
            response_text = ""
            agent_type_str = "supervisor"
            sources = []
            
            async for event in workflow.astream(initial_state):
                # Log the event for debugging
                logger.debug(f"[{session_id}] Event: {event}")
                
                # Check if this is a final result
                if "__end__" in event:
                    final_result = event["__end__"]
                    
                    # Extract final message
                    final_messages = final_result.get("messages", [])
                    if final_messages:
                        last_message = final_messages[-1]
                        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
                    
                    # Get routing decision
                    routing_decision = final_result.get("routing_decision", {})
                    agent_type_str = routing_decision.get("next_agent", "supervisor")
                    sources = routing_decision.get("sources", [])
                
                # Stream progress updates
                for node_name, node_output in event.items():
                    if node_name != "__end__":
                        progress = {
                            "type": "progress",
                            "node": node_name,
                        }
                        yield f"data: {json.dumps(progress)}\n\n"
            
            # Stream the final response (character by character for better UX)
            for i in range(0, len(response_text), 5):  # Stream in chunks of 5 chars
                chunk = response_text[i:i+5]
                chunk_data = {
                    "type": "content",
                    "content": chunk,
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
            
            # Send final completion message
            duration = (datetime.now() - start_time).total_seconds()
            completion = {
                "type": "complete",
                "agent_type": agent_type_str,
                "sources": sources,
                "session_id": session_id,
                "duration": duration,
            }
            yield f"data: {json.dumps(completion)}\n\n"
            
            logger.info(f"[{session_id}] Streaming completed in {duration:.2f}s by {agent_type_str} agent")
            
            # Add to session history
            add_to_session_history(session_id, {
                "role": "user",
                "content": request.message,
                "timestamp": start_time.isoformat(),
            })
            add_to_session_history(session_id, {
                "role": "assistant",
                "content": response_text,
                "agent_type": agent_type_str,
                "timestamp": datetime.now().isoformat(),
            })
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[{session_id}] Streaming failed after {duration:.2f}s: {str(e)}", exc_info=True)
            error_data = {
                "type": "error",
                "error": str(e),
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
    )


@router.get("/sessions/{session_id}/history")
async def get_history(session_id: str):
    """
    Get conversation history for a session
    """
    try:
        history = get_session_history(session_id)
        return {
            "session_id": session_id,
            "message_count": len(history),
            "history": history,
        }
    except Exception as e:
        logger.error(f"Error retrieving history for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clear conversation history for a session
    """
    try:
        if session_id in _session_histories:
            del _session_histories[session_id]
            logger.info(f"Cleared session {session_id}")
        return {
            "status": "success",
            "message": f"Session {session_id} cleared",
        }
    except Exception as e:
        logger.error(f"Error clearing session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

