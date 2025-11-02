"""
Supervisor Agent - Routes queries to specialized agents
Uses AWS Bedrock Claude Haiku for cost-effective routing
"""

from typing import Dict, Any
from langchain_core.messages import BaseMessage


class SupervisorAgent:
    """
    Supervisor agent that analyzes queries and routes to appropriate worker agents
    
    Strategy: Uses fast, cost-effective LLM (AWS Bedrock Claude Haiku) for routing decisions
    """
    
    def __init__(self):
        """Initialize supervisor agent"""
        # TODO: Initialize AWS Bedrock client in Stage 4
        pass
    
    def route_query(self, message: str, history: list[BaseMessage]) -> str:
        """
        Analyze user query and determine which agent should handle it
        
        Args:
            message: User's message
            history: Conversation history
            
        Returns:
            Agent name to route to: 'technical', 'configuration', or 'billing'
        """
        # TODO: Implement routing logic in Stage 5
        return "technical"
    
    def format_routing_prompt(self, message: str) -> str:
        """
        Create prompt for routing decision
        
        Args:
            message: User's message
            
        Returns:
            Formatted prompt for LLM
        """
        # TODO: Implement in Stage 5
        pass

