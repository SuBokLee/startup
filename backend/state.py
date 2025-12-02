"""
State definition for FounderOS LangGraph
"""

from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator


class AgentState(TypedDict):
    """
    State for the multi-agent system
    
    Attributes:
        messages: List of messages in the conversation
        next: Name of the next agent to execute (or "FINISH")
        last_agent: Name of the last agent that responded (for tracking)
    """
    messages: Annotated[List[BaseMessage], add_messages]
    next: str
    last_agent: str  # Track which agent responded

