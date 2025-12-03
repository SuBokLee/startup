"""
Tools for FounderOS Agents
"""

import os
from dotenv import load_dotenv
try:
    from langchain_tavily import TavilySearchResults
except ImportError:
    # Fallback to old import for compatibility
    from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv()


def get_search_tool(max_results: int = 3):
    """
    Initialize Tavily Search Tool
    
    Args:
        max_results: Maximum number of search results to return (default: 3)
    
    Returns:
        TavilySearchResults tool instance or None if API key not found
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Warning: TAVILY_API_KEY not found. Web search will not work.")
        return None
    
    return TavilySearchResults(
        max_results=max_results,
        api_key=api_key
    )


# Default search tool instance (lazy initialization)
_search_tool = None

def get_search_tool_instance():
    """Get or create search tool instance"""
    global _search_tool
    if _search_tool is None:
        _search_tool = get_search_tool(max_results=3)
    return _search_tool

# For backward compatibility
search_tool = get_search_tool_instance()

