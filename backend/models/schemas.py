"""
Pydantic models for API requests and responses
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Types of specialized agents"""
    TECHNICAL = "technical"
    CONFIGURATION = "configuration"
    BILLING = "billing"
    SUPERVISOR = "supervisor"


class Message(BaseModel):
    """Single message in the conversation"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    agent_type: Optional[AgentType] = Field(None, description="Which agent handled this message")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User's message", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    conversation_history: Optional[List[Message]] = Field(default_factory=list, description="Previous messages")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="AI assistant's response")
    agent_type: AgentType = Field(..., description="Which agent handled the request")
    session_id: str = Field(..., description="Session ID")
    sources: Optional[List[str]] = Field(default_factory=list, description="Source documents used (for RAG)")

