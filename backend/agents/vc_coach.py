"""
VC Simulator Agent
"""

from typing import Dict, Any
from .base import BaseAgent
from prompts import VC_COACH_PROMPT


class VCCoachAgent(BaseAgent):
    """VC Simulator: Pitch deck review, devil's advocate questions, investor matching"""
    
    def __init__(self):
        super().__init__(
            name="VC Simulator",
            system_prompt=VC_COACH_PROMPT
        )
    
    async def process(self, message: str, context: Dict[str, Any] = None) -> str:
        """Process message as VC coach"""
        context = context or {}
        conversation_history = context.get("history", [])
        
        messages = self._format_messages(message, conversation_history)
        
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            return f"[VC Simulator Error] {str(e)}"

