"""
LLM Configuration for FounderOS using Google Gemini
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()


def get_gemini_llm(model: str = "gemini-1.5-pro", temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """
    Initialize ChatGoogleGenerativeAI with Gemini model
    
    Args:
        model: Model name (default: "gemini-1.5-pro")
              Note: Do NOT include "models/" prefix - ChatGoogleGenerativeAI adds it automatically
              Use "gemini-1.5-pro" or "gemini-1.5-flash" (without version suffix)
        temperature: Temperature for generation (default: 0.7)
    
    Returns:
        ChatGoogleGenerativeAI instance
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    # Remove "models/" prefix if present (ChatGoogleGenerativeAI adds it automatically)
    if model.startswith("models/"):
        model = model.replace("models/", "")
    
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=api_key,
        convert_system_message_to_human=True  # Handle system messages properly
    )


# Default LLM instances
def get_supervisor_llm() -> ChatGoogleGenerativeAI:
    """Get LLM for Supervisor (faster routing)"""
    # Use gemini-1.5-flash for faster responses and better quota
    # Note: Do NOT include "models/" prefix or version suffix
    return get_gemini_llm(model="gemini-1.5-flash", temperature=0.3)


def get_agent_llm() -> ChatGoogleGenerativeAI:
    """Get LLM for Agents (high-quality reasoning)"""
    # Use gemini-1.5-pro for high-quality responses
    # If quota issues occur, can fallback to gemini-1.5-flash
    # Note: Do NOT include "models/" prefix or version suffix
    return get_gemini_llm(model="gemini-1.5-pro", temperature=0.7)

