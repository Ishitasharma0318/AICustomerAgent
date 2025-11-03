"""
Supervisor Agent - Routes queries to specialized agents
Uses AWS Bedrock Claude Haiku for cost-effective routing
"""

import os
import json
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Try to import AWS Bedrock, but make it optional
try:
    from langchain_aws import ChatBedrock
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False
    print("⚠️ langchain_aws not available - using keyword-based routing only")


class SupervisorAgent:
    """
    Supervisor agent that analyzes queries and routes to appropriate worker agents
    
    Strategy: Uses fast, cost-effective LLM (AWS Bedrock Claude Haiku) for routing decisions
    """
    
    def __init__(self, model_id: str = "anthropic.claude-3-haiku-20240307-v1:0", region_name: str = "us-east-1"):
        """
        Initialize supervisor agent
        
        Args:
            model_id: AWS Bedrock model ID (Claude Haiku for cost-effectiveness)
            region_name: AWS region for Bedrock
        """
        # Initialize AWS Bedrock client with Claude Haiku (fast and cost-effective)
        if BEDROCK_AVAILABLE:
            try:
                self.llm = ChatBedrock(
                    model_id=model_id,
                    region_name=region_name,
                    model_kwargs={
                        "temperature": 0.0,  # Deterministic routing
                        "max_tokens": 100,   # Short responses for routing
                    }
                )
                self.bedrock_available = True
            except Exception as e:
                print(f"⚠️ AWS Bedrock not available: {e}")
                print("⚠️ Falling back to keyword-based routing")
                self.llm = None
                self.bedrock_available = False
        else:
            print("⚠️ AWS Bedrock package not installed")
            print("⚠️ Using keyword-based routing")
            self.llm = None
            self.bedrock_available = False
        
        # Create routing prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_routing_prompt()),
            ("human", "{query}")
        ])
        
        # Create routing chain if Bedrock is available
        if self.bedrock_available:
            self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    def _get_routing_prompt(self) -> str:
        """Get the system prompt for routing decisions"""
        return """You are a routing supervisor for an AWS customer service system. Your job is to analyze user queries and route them to the appropriate specialist agent.

Available agents:
1. TECHNICAL - Handles troubleshooting, debugging, errors, and technical issues
   Examples: timeouts, 502 errors, cold starts, performance issues, debugging
   
2. CONFIGURATION - Handles best practices, security, architecture, and setup
   Examples: IAM policies, CORS setup, best practices, security guidelines, deployment
   
3. BILLING - Handles pricing, costs, billing, and cost optimization
   Examples: pricing questions, cost estimates, free tier, billing, cost optimization

Analyze the user's query and respond with ONLY ONE WORD:
- "technical" for troubleshooting/debugging questions
- "configuration" for best practices/setup questions  
- "billing" for pricing/cost questions

User Query: {query}

Route to (respond with one word only):"""
    
    async def route_query(self, message: str, history: List[BaseMessage]) -> Dict[str, Any]:
        """
        Analyze user query and determine which agent should handle it
        
        Args:
            message: User's message
            history: Conversation history
            
        Returns:
            Dict with routing decision and metadata
        """
        if self.bedrock_available:
            # Use AWS Bedrock for intelligent routing
            route_decision = await self._route_with_bedrock(message)
        else:
            # Fallback to keyword-based routing
            route_decision = self._route_with_keywords(message)
        
        return {
            "next_agent": route_decision["agent"],
            "confidence": route_decision.get("confidence", "medium"),
            "reasoning": route_decision.get("reasoning", ""),
            "routing_method": route_decision.get("method", "bedrock")
        }
    
    async def _route_with_bedrock(self, message: str) -> Dict[str, Any]:
        """
        Route query using AWS Bedrock Claude Haiku
        
        Args:
            message: User's message
            
        Returns:
            Routing decision dict
        """
        try:
            # Get routing decision from Bedrock
            response = await self.chain.ainvoke({"query": message})
            
            # Parse response (should be one word: technical, configuration, or billing)
            agent = response.strip().lower()
            
            # Validate response
            valid_agents = ["technical", "configuration", "billing"]
            if agent not in valid_agents:
                # If response is invalid, try to extract valid agent name
                for valid_agent in valid_agents:
                    if valid_agent in agent:
                        agent = valid_agent
                        break
                else:
                    # Default to technical if unclear
                    agent = "technical"
            
            return {
                "agent": agent,
                "confidence": "high",
                "reasoning": f"Bedrock routing: {response}",
                "method": "bedrock"
            }
        except Exception as e:
            print(f"⚠️ Bedrock routing failed: {e}, falling back to keywords")
            return self._route_with_keywords(message)
    
    def _route_with_keywords(self, message: str) -> Dict[str, Any]:
        """
        Fallback keyword-based routing (if Bedrock unavailable)
        
        Args:
            message: User's message
            
        Returns:
            Routing decision dict
        """
        message_lower = message.lower()
        
        # Billing keywords
        billing_keywords = [
            "cost", "price", "pricing", "bill", "billing", "charge", "free tier",
            "expensive", "cheaper", "budget", "estimate", "fees", "payment",
            "optimization", "save money", "how much"
        ]
        
        # Technical keywords
        technical_keywords = [
            "error", "timeout", "fail", "not working", "broken", "bug", "debug",
            "502", "504", "500", "400", "cold start", "performance", "slow",
            "issue", "problem", "troubleshoot", "fix", "crashed", "exception"
        ]
        
        # Configuration keywords
        configuration_keywords = [
            "configure", "setup", "best practice", "security", "iam", "policy",
            "cors", "deploy", "architecture", "how to", "guideline", "recommendation",
            "pattern", "strategy", "design", "environment", "configuration"
        ]
        
        # Count keyword matches
        billing_score = sum(1 for kw in billing_keywords if kw in message_lower)
        technical_score = sum(1 for kw in technical_keywords if kw in message_lower)
        config_score = sum(1 for kw in configuration_keywords if kw in message_lower)
        
        # Determine routing based on scores
        if billing_score > technical_score and billing_score > config_score:
            agent = "billing"
        elif technical_score > config_score:
            agent = "technical"
        else:
            agent = "configuration"
        
        return {
            "agent": agent,
            "confidence": "medium",
            "reasoning": f"Keyword match: billing={billing_score}, technical={technical_score}, config={config_score}",
            "method": "keyword"
        }
    
    def format_routing_prompt(self, message: str) -> str:
        """
        Create prompt for routing decision
        
        Args:
            message: User's message
            
        Returns:
            Formatted prompt for LLM
        """
        return self._get_routing_prompt().format(query=message)

