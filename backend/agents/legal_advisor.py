"""
Legal Advisor Agent - Startup Legal Specialist
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState


# System prompt for the Legal Advisor Agent
LEGAL_ADVISOR_SYSTEM_PROMPT = """You are a specialized Startup Legal Advisor.

Your tasks are:
1. **Drafting:** Create standard legal documents (NDA, MOU, Service Agreements, Employment Contracts) suitable for Korean startups. Use formal legal terminology.
2. **Reviewing:** Analyze clauses provided by the user. Point out 'toxic clauses' or risks (e.g., broad indemnification, non-compete clauses without compensation).

**CRITICAL RULE:** You MUST append a disclaimer at the end of every response:

> **⚠️ 면책 조항:** 이 내용은 법률 자문이 아니며, 참고용으로만 사용해야 합니다. 실제 계약 체결 시 반드시 변호사의 검토를 받으시기 바랍니다.

Key principles:
- Use formal legal terminology appropriate for Korean law
- Be thorough but clear in explanations
- Highlight potential risks and red flags
- Provide practical advice for early-stage startups
- Always include the disclaimer at the end

Always respond in Korean unless the user asks otherwise."""


def legal_advisor_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the Legal Advisor Agent
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with agent response
    """
    llm = get_agent_llm()
    
    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return {"next": "FINISH", "last_agent": "legal_advisor"}
    
    # Format messages with system prompt
    formatted_messages = [SystemMessage(content=LEGAL_ADVISOR_SYSTEM_PROMPT)]
    
    # Add conversation history
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            formatted_messages.append(AIMessage(content=msg.content))
    
    # Invoke LLM
    try:
        response = llm.invoke(formatted_messages)
        
        # Ensure disclaimer is included
        response_content = response.content
        if "면책 조항" not in response_content and "면책조항" not in response_content:
            disclaimer = "\n\n---\n\n**⚠️ 면책 조항:** 이 내용은 법률 자문이 아니며, 참고용으로만 사용해야 합니다. 실제 계약 체결 시 반드시 변호사의 검토를 받으시기 바랍니다."
            response_content = response_content + disclaimer
        
        # Add response to messages and finish
        return {
            "messages": [AIMessage(content=response_content)],
            "next": "FINISH",
            "last_agent": "legal_advisor"
        }
    except Exception as e:
        error_message = f"[Legal Advisor Agent Error] {str(e)}"
        return {
            "messages": [AIMessage(content=error_message)],
            "next": "FINISH",
            "last_agent": "legal_advisor"
        }

