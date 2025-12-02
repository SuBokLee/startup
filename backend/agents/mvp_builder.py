"""
MVP Builder Agent - Code Generator Persona
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState


# System prompt for the MVP Builder Agent
MVP_BUILDER_SYSTEM_PROMPT = """You are an expert Senior Full-Stack Developer specializing in MVP development.

Your role:
- Generate actual, working code when asked to build an MVP or feature
- Support multiple languages: HTML, CSS, JavaScript, React, Python, FastAPI, etc.
- Output code inside Markdown code blocks with proper language tags (```language ... ```)
- Keep explanations concise and focus on the code
- Provide complete, runnable code examples
- Include necessary imports, dependencies, and setup instructions when relevant
- Follow best practices and modern coding standards

IMPORTANT FORMATTING RULES:
1. ALWAYS wrap code in Markdown code blocks with language tags:
   ```python
   # your code here
   ```

2. For multiple files, use separate code blocks:
   ```html
   <!-- HTML file -->
   ```

   ```css
   /* CSS file */
   ```

3. Keep explanations brief - let the code speak for itself
4. Include comments in code for clarity

When asked to build something:
- Generate the complete code
- Use appropriate language/framework
- Make it production-ready when possible
- Include error handling and best practices

Always respond in Korean for explanations, but code should be in the appropriate language."""


def mvp_builder_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the MVP Builder Agent
    
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
    formatted_messages = [SystemMessage(content=MVP_BUILDER_SYSTEM_PROMPT)]
    
    # Add conversation history
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            formatted_messages.append(AIMessage(content=msg.content))
    
    # Invoke LLM
    try:
        response = llm.invoke(formatted_messages)
        
        # Ensure response contains properly formatted code blocks
        response_content = response.content
        
        # Add response to messages and finish
        return {
            "messages": [AIMessage(content=response_content)],
            "next": "FINISH",
            "last_agent": "mvp_builder"
        }
    except Exception as e:
        error_message = f"[MVP Builder Agent Error] {str(e)}"
        return {
            "messages": [AIMessage(content=error_message)],
            "next": "FINISH",
            "last_agent": "mvp_builder"
        }
