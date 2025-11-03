"""
Supervisor Agent - Routes queries to specialized agents using AWS Bedrock Claude Haiku
Cost: ~$0.00001 per routing | Speed: ~150-200ms | Accuracy: High
"""

import os
import json
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Try to import AWS Bedrock - gracefully fallback if not available
try:
    from langchain_aws import ChatBedrock
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False
    print("⚠️ AWS Bedrock not available - using keyword-based routing fallback")


class SupervisorAgent:
    """Routes customer queries to specialized agents (Technical, Configuration, or Billing)"""
    
    def __init__(
        self, 
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0", 
        region_name: str = "us-east-1"
    ):
        """Initialize supervisor with AWS Bedrock Claude Haiku for cost-effective routing"""
        
        # Initialize AWS Bedrock LLM (Claude Haiku - fast and cheap for classification)
        if BEDROCK_AVAILABLE:
            try:
                self.llm = ChatBedrock(
                    model_id=model_id,
                    region_name=region_name,
                    model_kwargs={
                        "temperature": 0.0,  # Deterministic routing
                        "max_tokens": 100,   # Only need one word response
                    }
                )
                self.bedrock_available = True
                print("✅ AWS Bedrock Claude Haiku initialized for routing")
            except Exception as e:
                print(f"⚠️ AWS Bedrock initialization failed: {e}")
                print("⚠️ Falling back to keyword-based routing")
                self.llm = None
                self.bedrock_available = False
        else:
            self.llm = None
            self.bedrock_available = False
        
        # Create LangChain prompt template for routing
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_routing_prompt()),
            ("human", "{query}")
        ])
        
        # Create LCEL chain: Prompt → Bedrock → String Parser
        if self.bedrock_available:
            self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    def _get_routing_prompt(self) -> str:
        """Get system prompt that instructs Bedrock to classify queries into technical, configuration, or billing"""
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
        Main routing method - analyzes query and returns which agent should handle it
        Uses Bedrock if available, falls back to keyword matching otherwise
        """
        # Try Bedrock routing first, fallback to keywords if unavailable
        if self.bedrock_available:
            route_decision = await self._route_with_bedrock(message)
        else:
            route_decision = self._route_with_keywords(message)
        
        return {
            "next_agent": route_decision["agent"],
            "confidence": route_decision.get("confidence", "medium"),
            "reasoning": route_decision.get("reasoning", ""),
            "routing_method": route_decision.get("method", "bedrock")
        }
    
    async def _route_with_bedrock(self, message: str) -> Dict[str, Any]:
        """Use AWS Bedrock Claude Haiku for intelligent query classification (~$0.00001 per routing)"""
        try:
            # Call Bedrock via LCEL chain
            response = await self.chain.ainvoke({"query": message})
            agent = response.strip().lower()
            
            # Validate response is a valid agent
            valid_agents = ["technical", "configuration", "billing"]
            if agent not in valid_agents:
                for valid_agent in valid_agents:
                    if valid_agent in agent:
                        agent = valid_agent
                        break
                else:
                    agent = "technical"  # Default fallback
            
            print(f"✅ Bedrock routing: '{message[:50]}...' → {agent}")
            
            return {
                "agent": agent,
                "confidence": "high",
                "reasoning": f"Bedrock classification: {response}",
                "method": "bedrock"
            }
            
        except Exception as e:
            print(f"⚠️ Bedrock routing error: {e}")
            print(f"⚠️ Falling back to keyword-based routing")
            return self._route_with_keywords(message)
    
    def _route_with_keywords(self, message: str) -> Dict[str, Any]:
        """Fallback keyword-based routing - counts keyword matches for each category"""
        message_lower = message.lower()
        
        # Define keyword lists for each category
        billing_keywords = [
            "cost", "price", "pricing", "bill", "billing", "charge", "free tier",
            "expensive", "cheaper", "budget", "estimate", "fees", "payment",
            "optimization", "save money", "how much"
        ]
        
        technical_keywords = [
            "error", "timeout", "fail", "not working", "broken", "bug", "debug",
            "502", "504", "500", "400", "cold start", "performance", "slow",
            "issue", "problem", "troubleshoot", "fix", "crashed", "exception"
        ]
        
        configuration_keywords = [
            "configure", "setup", "best practice", "security", "iam", "policy",
            "cors", "deploy", "architecture", "how to", "guideline", "recommendation",
            "pattern", "strategy", "design", "environment", "configuration"
        ]
        
        # Count keyword matches for each category
        billing_score = sum(1 for kw in billing_keywords if kw in message_lower)
        technical_score = sum(1 for kw in technical_keywords if kw in message_lower)
        config_score = sum(1 for kw in configuration_keywords if kw in message_lower)
        
        # Route to category with highest score
        if billing_score > technical_score and billing_score > config_score:
            agent = "billing"
        elif technical_score > config_score:
            agent = "technical"
        else:
            agent = "configuration"
        
        print(f"📝 Keyword routing: '{message[:50]}...' → {agent} " + 
              f"(scores: billing={billing_score}, technical={technical_score}, config={config_score})")
        
        return {
            "agent": agent,
            "confidence": "medium",
            "reasoning": f"Keyword scores: billing={billing_score}, technical={technical_score}, config={config_score}",
            "method": "keyword"
        }
    
    def format_routing_prompt(self, message: str) -> str:
        """Helper method to format routing prompt for debugging/testing"""
        return self._get_routing_prompt().format(query=message)

