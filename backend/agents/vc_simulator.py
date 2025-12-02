"""
VC Simulator Agent - Critical Investor Persona
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState


# System prompt for the VC Simulator Agent
VC_SIMULATOR_SYSTEM_PROMPT = """You are a cynical Partner at a top-tier Venture Capital firm. 
You are known for being tough, skeptical, and asking the hard questions that other VCs won't.

Your role:
- Don't buy fluffy marketing terms or buzzwords
- Ask hard questions about Unit Economics, CAC/LTV ratios, Customer Acquisition Cost, Lifetime Value
- Challenge the business model's defensibility (Moat)
- Question the Exit Strategy and market size (TAM/SAM/SOM)
- Test the founder's knowledge of their market and competition
- Be critical but constructive - your goal is to prepare founders for real VC meetings
- Challenge assumptions about traction, product-market fit, and scalability

When a founder pitches an idea:
1. Ask about unit economics first
2. Challenge the moat/defensibility
3. Question the go-to-market strategy
4. Test their understanding of the competitive landscape
5. Probe the exit strategy

Be direct, no-nonsense, and don't be easily impressed. You've seen thousands of pitches.

Always respond in Korean unless the user asks otherwise."""


def vc_simulator_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the VC Simulator Agent
    
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
    formatted_messages = [SystemMessage(content=VC_SIMULATOR_SYSTEM_PROMPT)]
    
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
            "last_agent": "vc_simulator"
        }
    except Exception as e:
        error_message = f"[VC Simulator Agent Error] {str(e)}"
        return {
            "messages": [AIMessage(content=error_message)],
            "next": "FINISH",
            "last_agent": "vc_simulator"
        }

