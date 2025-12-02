"""
Market Sensor Agent - Analyzes competitors and market trends
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState
from tools import get_search_tool_instance


# System prompt for the Market Sensor Agent
MARKET_SENSOR_SYSTEM_PROMPT = """You are a Market Intelligence Analyst specializing in competitive analysis and market trends.

Your role:
- Search for and analyze competitors in the user's market
- Find recent news, customer reviews, and industry trends
- Identify market gaps and opportunities
- Provide competitive intelligence and strategic insights
- Analyze market sentiment and emerging trends

IMPORTANT: You MUST use the search tool to find current market information, competitor data, and recent news. 
Do not rely on general knowledge alone - always search for the latest information.

Always respond in Korean unless the user asks otherwise."""


def market_sensor_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the Market Sensor Agent with web search capability
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with agent response
    """
    llm = get_agent_llm()
    
    # Get search tool (may be None if API key not set)
    search_tool = get_search_tool_instance()
    
    # Bind the search tool to the LLM if available
    if search_tool:
        llm_with_tools = llm.bind_tools([search_tool])
    else:
        llm_with_tools = llm
    
    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return {"next": "FINISH"}
    
    # Format messages with system prompt
    formatted_messages = [SystemMessage(content=MARKET_SENSOR_SYSTEM_PROMPT)]
    
    # Add conversation history
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            formatted_messages.append(AIMessage(content=msg.content))
        elif isinstance(msg, ToolMessage):
            formatted_messages.append(msg)
    
    try:
        # First invocation - LLM may decide to use the tool
        response = llm_with_tools.invoke(formatted_messages)
        
        # Check if the LLM wants to use a tool
        # Gemini uses response.tool_calls or response.additional_kwargs.get("tool_calls")
        tool_calls = getattr(response, 'tool_calls', []) or response.additional_kwargs.get("tool_calls", [])
        
        if tool_calls:
            # Execute tool calls
            tool_messages = []
            for tool_call in tool_calls:
                # Handle different tool call formats
                if isinstance(tool_call, dict):
                    tool_name = tool_call.get("name") or tool_call.get("function", {}).get("name")
                    tool_args = tool_call.get("args") or tool_call.get("function", {}).get("arguments", {})
                    tool_id = tool_call.get("id") or tool_call.get("function", {}).get("name")
                else:
                    tool_name = getattr(tool_call, "name", None)
                    tool_args = getattr(tool_call, "args", {})
                    tool_id = getattr(tool_call, "id", None)
                
                # Parse tool_args if it's a string
                if isinstance(tool_args, str):
                    import json
                    try:
                        tool_args = json.loads(tool_args)
                    except:
                        tool_args = {"query": tool_args}
                
                if tool_name == "tavily_search_results_json" or "tavily" in str(tool_name).lower():
                    # Execute search
                    search_result = search_tool.invoke(tool_args)
                    tool_messages.append(
                        ToolMessage(
                            content=str(search_result),
                            tool_call_id=tool_id or "search"
                        )
                    )
            
            # Add tool messages and get final response
            formatted_messages.append(response)
            formatted_messages.extend(tool_messages)
            
            # Get final response from LLM with tool results
            final_response = llm.invoke(formatted_messages)
            
            return {
                "messages": [AIMessage(content=final_response.content)],
                "next": "FINISH",
                "last_agent": "market_sensor"
            }
        else:
            # No tool calls, return direct response
            return {
                "messages": [AIMessage(content=response.content)],
                "next": "FINISH",
                "last_agent": "market_sensor"
            }
    
    except Exception as e:
        error_message = f"[Market Sensor Agent Error] {str(e)}"
        return {
            "messages": [AIMessage(content=error_message)],
            "next": "FINISH",
            "last_agent": "market_sensor"
        }
