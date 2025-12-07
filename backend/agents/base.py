"""
Base agent class for all FounderOS agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage


class BaseAgent(ABC):
    """Base class for all specialist agents"""
    
    def __init__(self, name: str, system_prompt: str, model_name: str = "gemini-pro"):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    
    @abstractmethod
    async def process(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Process a message and return a response
        
        Args:
            message: User's message
            context: Additional context (conversation history, etc.)
        
        Returns:
            Agent's response
        """
        pass
    
    def _format_messages(self, user_message: str, conversation_history: list = None) -> list:
        """Format messages for LLM input"""
        from langchain.schema import SystemMessage, HumanMessage, AIMessage
        
        messages = [SystemMessage(content=self.system_prompt)]
        
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=msg.get("content", "")))
        
        messages.append(HumanMessage(content=user_message))
        return messages

