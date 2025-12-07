"""
LLM Configuration for FounderOS using Google Gemini
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()


def get_gemini_llm(model: str = "gemini-1.5-flash-latest", temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """
    Initialize ChatGoogleGenerativeAI with Gemini model
    
    Args:
        model: Model name (default: "gemini-1.5-pro")
        temperature: Temperature for generation (default: 0.7)
    
    Returns:
        ChatGoogleGenerativeAI instance
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=api_key,
        convert_system_message_to_human=True  # Handle system messages properly
    )


# Default LLM instances
def get_supervisor_llm() -> ChatGoogleGenerativeAI:
    """Get LLM for Supervisor (faster routing)"""
    # Use gemini-1.5-flash-latest for compatibility
    return get_gemini_llm(model="gemini-1.5-flash-latest", temperature=0.3)


def get_agent_llm() -> ChatGoogleGenerativeAI:
    """Get LLM for Agents (high-quality reasoning)"""
    # Use gemini-1.5-flash-latest for better quota limits and compatibility
    # This model has better quota limits for free tier
    return get_gemini_llm(model="gemini-1.5-flash-latest", temperature=0.7)

