"""
Growth Hacker Agent - Marketing and Growth Specialist
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState


# System prompt for the Growth Hacker Agent
GROWTH_HACKER_SYSTEM_PROMPT = """You are a Growth Hacker specializing in early-stage startups.

Your goal is to maximize conversion and viral reach with zero budget.

You can write:
1. **Cold Emails** (Concise, value-driven, high open rate)
2. **Social Media Posts** (LinkedIn, Twitter, Instagram - engaging hooks)
3. **Blog Posts** (SEO-optimized, storytelling)

Always ask for the target audience and platform before writing.

Key principles:
- Focus on value-first messaging
- Use data-driven copywriting techniques
- Create content that encourages sharing
- Optimize for engagement and conversion
- Be creative but practical

Always respond in Korean unless the user asks otherwise."""


def growth_hacker_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the Growth Hacker Agent
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with agent response
    """
    llm = get_agent_llm()
    
    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return {"next": "FINISH", "last_agent": "growth_hacker"}
    
    # Format messages with system prompt
    formatted_messages = [SystemMessage(content=GROWTH_HACKER_SYSTEM_PROMPT)]
    
    # Add conversation history
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            formatted_messages.append(AIMessage(content=msg.content))
    
    # Invoke LLM
    try:
        response = llm.invoke(formatted_messages)
        
        # Add response to messages and finish
        return {
            "messages": [AIMessage(content=response.content)],
            "next": "FINISH",
            "last_agent": "growth_hacker"
        }
    except Exception as e:
        error_message = f"[Growth Hacker Agent Error] {str(e)}"
        return {
            "messages": [AIMessage(content=error_message)],
            "next": "FINISH",
            "last_agent": "growth_hacker"
        }

