"""
Virtual Co-founder Agent
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState


# System prompt for the Cofounder Agent
COFOUNDER_SYSTEM_PROMPT = """You are a pragmatic Virtual Co-founder. You help startup founders refine their ideas using frameworks like Lean Canvas. 
You challenge assumptions logically and provide constructive feedback.

Your role:
- Help refine business ideas using proven frameworks (Lean Canvas, Business Model Canvas)
- Challenge assumptions with logical reasoning
- Provide actionable advice for startup founders
- Be supportive but honest
- Focus on practical, implementable solutions

Always respond in Korean unless the user asks otherwise."""


def cofounder_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the Cofounder Agent
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with agent response
    """
    llm = get_agent_llm()
    
    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return {"next": "FINISH"}
    
    # Format messages with system prompt
    formatted_messages = [SystemMessage(content=COFOUNDER_SYSTEM_PROMPT)]
    
    # Add conversation history
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            formatted_messages.append(AIMessage(content=msg.content))
    
    # Invoke LLM
    try:
        response = llm.invoke(formatted_messages)
        
        # Add response to messages and finish (supervisor will handle next user message)
        return {
            "messages": [AIMessage(content=response.content)],
            "next": "FINISH",  # Finish after responding, wait for next user message
            "last_agent": "cofounder"  # Track which agent responded
        }
    except Exception as e:
        error_message = f"[Cofounder Agent Error] {str(e)}"
        return {
            "messages": [AIMessage(content=error_message)],
            "next": "FINISH",
            "last_agent": "cofounder"
        }
