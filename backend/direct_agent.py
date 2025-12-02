"""
Direct agent routing - bypass supervisor when agent is specified
"""

from langchain_core.messages import HumanMessage, AIMessage
from state import AgentState
from agents.cofounder import cofounder_node
from agents.vc_simulator import vc_simulator_node
from agents.grant_hunter import grant_hunter_node
from agents.market_sensor import market_sensor_node
from agents.mvp_builder import mvp_builder_node
from agents.framework_designer import framework_designer_node
from agents.growth_hacker import growth_hacker_node
from agents.legal_advisor import legal_advisor_node


# Agent node mapping
AGENT_NODES = {
    "cofounder": cofounder_node,
    "vc_simulator": vc_simulator_node,
    "grant_hunter": grant_hunter_node,
    "market_sensor": market_sensor_node,
    "mvp_builder": mvp_builder_node,
    "framework_designer": framework_designer_node,
    "growth_hacker": growth_hacker_node,
    "legal_advisor": legal_advisor_node,
}


async def route_to_agent(agent_name: str, message: str, thread_id: str, graph_with_memory):
    """
    Route directly to specified agent, bypassing supervisor
    
    Args:
        agent_name: Name of the agent to route to
        message: User message
        thread_id: Conversation thread ID
        graph_with_memory: Compiled graph with memory (for memory access)
    
    Returns:
        Agent response
    """
    if agent_name not in AGENT_NODES:
        raise ValueError(f"Unknown agent: {agent_name}")
    
    # Create config for this thread
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 50
    }
    
    # Get conversation history from memory if available
    try:
        # Get current state from memory
        current_state = graph_with_memory.get_state(config)
        existing_messages = current_state.values.get("messages", []) if current_state else []
    except:
        existing_messages = []
    
    # Add new user message
    all_messages = list(existing_messages) + [HumanMessage(content=message)]
    
    # Get the agent node function
    agent_node = AGENT_NODES[agent_name]
    
    # Create state with all messages
    agent_state: AgentState = {
        "messages": all_messages,
        "next": "FINISH"
    }
    
    # Invoke the agent directly
    result = agent_node(agent_state)
    
    # Update memory with new messages
    try:
        graph_with_memory.update_state(config, result)
    except:
        pass  # If memory update fails, continue anyway
    
    # Get the response
    messages = result.get("messages", [])
    last_message = messages[-1] if messages else None
    
    response_text = last_message.content if last_message else "No response generated"
    
    return {
        "response": response_text,
        "agent": agent_name,
        "thread_id": thread_id
    }

