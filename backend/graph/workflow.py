"""
LangGraph workflow implementation
Orchestrates the multi-agent system
"""

import sys
import os
from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

# Add parent directory to path to import agents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.state import AgentState
from agents.supervisor import SupervisorAgent
from agents.technical_agent import TechnicalSupportAgent
from agents.configuration_agent import ConfigurationAgent
from agents.billing_agent import BillingAgent


# Global agent instances (initialized once)
_supervisor = None
_technical_agent = None
_configuration_agent = None
_billing_agent = None


def get_agents():
    """Initialize and return singleton agent instances"""
    global _supervisor, _technical_agent, _configuration_agent, _billing_agent
    
    if _supervisor is None:
        _supervisor = SupervisorAgent()
    if _technical_agent is None:
        _technical_agent = TechnicalSupportAgent()
    if _configuration_agent is None:
        _configuration_agent = ConfigurationAgent()
    if _billing_agent is None:
        _billing_agent = BillingAgent()
    
    return _supervisor, _technical_agent, _configuration_agent, _billing_agent


def create_workflow():
    """
    Create the LangGraph workflow for multi-agent orchestration
    
    Returns:
        Compiled workflow graph
    """
    # Define the workflow graph
    workflow = StateGraph(AgentState)
    
    # Define nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("technical", technical_node)
    workflow.add_node("configuration", configuration_node)
    workflow.add_node("billing", billing_node)
    
    # Define edges
    workflow.set_entry_point("supervisor")
    
    # Conditional edges from supervisor to workers
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "technical": "technical",
            "configuration": "configuration",
            "billing": "billing",
            "end": END,
        }
    )
    
    # All workers return to END
    workflow.add_edge("technical", END)
    workflow.add_edge("configuration", END)
    workflow.add_edge("billing", END)
    
    # Compile and return
    return workflow.compile()


async def supervisor_node(state: AgentState) -> AgentState:
    """
    Supervisor node - routes queries to appropriate agent
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with routing decision
    """
    supervisor, _, _, _ = get_agents()
    
    # Get the latest user message
    messages = state.get("messages", [])
    if not messages:
        return {
            **state,
            "next_agent": "end",
            "routing_decision": {"error": "No messages to route"}
        }
    
    latest_message = messages[-1]
    message_content = latest_message.content if hasattr(latest_message, 'content') else str(latest_message)
    
    # Route the query
    routing_decision = await supervisor.route_query(message_content, messages)
    
    # Update state with routing decision
    return {
        **state,
        "next_agent": routing_decision["next_agent"],
        "routing_decision": routing_decision
    }


async def technical_node(state: AgentState) -> AgentState:
    """
    Technical support node
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with technical response
    """
    _, technical_agent, _, _ = get_agents()
    
    # Get the latest user message
    messages = state.get("messages", [])
    latest_message = messages[-1]
    message_content = latest_message.content if hasattr(latest_message, 'content') else str(latest_message)
    
    # Get session ID
    session_id = state.get("session_id", "default")
    
    # Process the query
    response = await technical_agent.process(message_content, messages, session_id)
    
    # Create AI message with response
    ai_message = AIMessage(content=response["response"])
    
    # Update state
    return {
        **state,
        "messages": [ai_message],
        "next_agent": "end"
    }


async def configuration_node(state: AgentState) -> AgentState:
    """
    Configuration agent node
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with configuration response
    """
    _, _, configuration_agent, _ = get_agents()
    
    # Get the latest user message
    messages = state.get("messages", [])
    latest_message = messages[-1]
    message_content = latest_message.content if hasattr(latest_message, 'content') else str(latest_message)
    
    # Get session ID
    session_id = state.get("session_id", "default")
    
    # Process the query
    response = await configuration_agent.process(message_content, messages, session_id)
    
    # Create AI message with response
    ai_message = AIMessage(content=response["response"])
    
    # Update state
    return {
        **state,
        "messages": [ai_message],
        "next_agent": "end"
    }


async def billing_node(state: AgentState) -> AgentState:
    """
    Billing agent node
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with billing response
    """
    _, _, _, billing_agent = get_agents()
    
    # Get the latest user message
    messages = state.get("messages", [])
    latest_message = messages[-1]
    message_content = latest_message.content if hasattr(latest_message, 'content') else str(latest_message)
    
    # Get session ID
    session_id = state.get("session_id", "default")
    
    # Process the query
    response = await billing_agent.process(message_content, messages, session_id)
    
    # Create AI message with response
    ai_message = AIMessage(content=response["response"])
    
    # Update state
    return {
        **state,
        "messages": [ai_message],
        "next_agent": "end"
    }


def route_to_agent(state: AgentState) -> Literal["technical", "configuration", "billing", "end"]:
    """
    Routing function to determine next agent
    
    Args:
        state: Current agent state
        
    Returns:
        Name of next agent to route to
    """
    next_agent = state.get("next_agent", "end")
    
    if next_agent in ["technical", "configuration", "billing"]:
        return next_agent
    
    return "end"

