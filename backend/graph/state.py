"""
State management for LangGraph workflow
"""

from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from operator import add


class AgentState(TypedDict):
    """
    State that flows through the LangGraph workflow
    
    Attributes:
        messages: List of messages in the conversation
        next_agent: Which agent should handle the next step
        session_id: Unique session identifier
        cached_data: Cached data for CAG and hybrid agents
        routing_decision: Supervisor's routing decision and reasoning
    """
    # Messages accumulate over the conversation
    messages: Annotated[Sequence[BaseMessage], add]
    
    # Which agent should process next
    next_agent: str
    
    # Session management
    session_id: str
    
    # Cached data for CAG/Hybrid agents
    cached_data: Optional[dict]
    
    # Routing metadata
    routing_decision: Optional[dict]


class MessageType:
    """Constants for message types"""
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"

