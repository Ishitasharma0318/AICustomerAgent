"""
LangGraph workflow implementation
Orchestrates the multi-agent system
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from .state import AgentState
from agents import SupervisorAgent, TechnicalSupportAgent, ConfigurationAgent, BillingAgent


def create_workflow():
    """
    Create the LangGraph workflow for multi-agent orchestration
    
    Returns:
        Compiled workflow graph
    """
    # Initialize agents
    supervisor = SupervisorAgent()
    technical_agent = TechnicalSupportAgent()
    configuration_agent = ConfigurationAgent()
    billing_agent = BillingAgent()
    
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
    
    # TODO: Compile and return in Stage 5
    # return workflow.compile()
    
    return workflow


def supervisor_node(state: AgentState) -> AgentState:
    """
    Supervisor node - routes queries to appropriate agent
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with routing decision
    """
    # TODO: Implement in Stage 5
    pass


def technical_node(state: AgentState) -> AgentState:
    """
    Technical support node
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with technical response
    """
    # TODO: Implement in Stage 4-5
    pass


def configuration_node(state: AgentState) -> AgentState:
    """
    Configuration agent node
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with configuration response
    """
    # TODO: Implement in Stage 4-5
    pass


def billing_node(state: AgentState) -> AgentState:
    """
    Billing agent node
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with billing response
    """
    # TODO: Implement in Stage 4-5
    pass


def route_to_agent(state: AgentState) -> Literal["technical", "configuration", "billing", "end"]:
    """
    Routing function to determine next agent
    
    Args:
        state: Current agent state
        
    Returns:
        Name of next agent to route to
    """
    # TODO: Implement routing logic in Stage 5
    next_agent = state.get("next_agent", "technical")
    
    if next_agent in ["technical", "configuration", "billing"]:
        return next_agent
    
    return "end"

