"""
Framework Designer Agent - Creates structured business frameworks
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_agent_llm
from state import AgentState
from models import LeanCanvasData, BusinessModelCanvasData


# System prompt for the Framework Designer Agent
FRAMEWORK_DESIGNER_SYSTEM_PROMPT = """You are an expert business strategist specializing in creating structured business frameworks.

Your role:
- Analyze the user's business idea and extract key information
- Fill in business framework canvases (Lean Canvas, Business Model Canvas) with concise, accurate information
- Focus on clarity and actionable insights
- Use the structured output format to ensure consistency

When creating a canvas:
- Be specific and concrete, not vague
- Fill all required fields
- Keep descriptions concise but informative
- Base content on the user's actual business idea

CRITICAL: All canvas field values MUST be written in Korean (한국어). Do not use English for the actual content values. Only use Korean text for all fields."""


def framework_designer_node(state: AgentState) -> Dict[str, Any]:
    """
    Process message through the Framework Designer Agent
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with structured canvas data
    """
    llm = get_agent_llm()
    
    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return {"next": "FINISH"}
    
    # Get the last user message
    last_message = messages[-1]
    user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    # Determine which canvas is requested
    user_message_lower = user_message.lower()
    is_lean_canvas = any(keyword in user_message_lower for keyword in ["lean canvas", "린 캔버스", "린캔버스"])
    is_bmc = any(keyword in user_message_lower for keyword in ["business model canvas", "bmc", "비즈니스 모델 캔버스", "비즈니스모델캔버스"])
    
    # Format messages with system prompt
    formatted_messages = [SystemMessage(content=FRAMEWORK_DESIGNER_SYSTEM_PROMPT)]
    
    # Add conversation history
    for msg in messages[:-1]:  # Exclude the last message as we'll add it separately
        if isinstance(msg, HumanMessage):
            formatted_messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            formatted_messages.append(AIMessage(content=msg.content))
    
    # Add the current user message with specific instruction
    if is_lean_canvas:
        canvas_instruction = f"""사용자의 비즈니스 아이디어를 분석하여 Lean Canvas를 작성해주세요.

사용자 메시지: {user_message}

Lean Canvas의 9개 블록을 모두 채워주세요. **모든 내용은 반드시 한국어로 작성해주세요.**

1. Problem (문제) - 고객이 직면한 상위 3가지 문제
2. Solution (해결책) - 해결책의 상위 3가지 기능
3. Unique Value Proposition (고유 가치 제안) - 당신이 다르고 구매할 가치가 있는 이유를 명확하게 전달하는 단일 메시지
4. Unfair Advantage (불공정한 우위) - 쉽게 복사하거나 구매할 수 없는 것
5. Customer Segments (고객 세그먼트) - 타겟 고객과 사용자
6. Key Metrics (핵심 지표) - 비즈니스가 어떻게 진행되고 있는지 알려주는 핵심 숫자
7. Channels (채널) - 고객에게 도달하는 경로
8. Cost Structure (비용 구조) - 고객 획득 비용, 유통 비용, 호스팅, 인력 등
9. Revenue Streams (수익원) - 수익 모델, 고객 생애 가치, 수익, 총 마진

**중요: 모든 필드의 내용은 반드시 한국어로 작성해야 합니다. 영어를 사용하지 마세요.**"""
        formatted_messages.append(HumanMessage(content=canvas_instruction))
        
        try:
            # Use structured output for Lean Canvas
            structured_llm = llm.with_structured_output(LeanCanvasData)
            canvas_data = structured_llm.invoke(formatted_messages)
            
            # Convert to JSON string for transmission
            canvas_json = {
                "type": "lean_canvas",
                "data": canvas_data.model_dump()
            }
            
            return {
                "messages": [AIMessage(content=json.dumps(canvas_json, ensure_ascii=False))],
                "next": "FINISH",
                "last_agent": "framework_designer"
            }
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                error_message = """⚠️ **API 할당량 초과**

현재 Google Gemini API의 무료 티어 할당량을 초과했습니다.

**해결 방법:**
1. 잠시 후 다시 시도해주세요 (약 1분 대기)
2. Google AI Studio에서 할당량 확인: https://ai.dev/usage
3. 필요시 유료 플랜으로 업그레이드 고려

불편을 드려 죄송합니다."""
            else:
                error_message = f"⚠️ **프레임워크 디자이너 오류**\n\n{error_str}\n\n잠시 후 다시 시도해주세요."
            return {
                "messages": [AIMessage(content=error_message)],
                "next": "FINISH",
                "last_agent": "framework_designer"
            }
    
    elif is_bmc:
        canvas_instruction = f"""사용자의 비즈니스 아이디어를 분석하여 Business Model Canvas를 작성해주세요.

사용자 메시지: {user_message}

Business Model Canvas의 9개 블록을 모두 채워주세요. **모든 내용은 반드시 한국어로 작성해주세요.**

1. Key Partners (핵심 파트너) - 핵심 파트너/공급업체는 누구인가요? 어떤 핵심 자원을 그들로부터 획득하나요?
2. Key Activities (핵심 활동) - 가치 제안을 위해 필요한 핵심 활동은 무엇인가요?
3. Key Resources (핵심 자원) - 가치 제안을 위해 필요한 핵심 자원은 무엇인가요?
4. Value Propositions (가치 제안) - 고객에게 제공하는 가치는 무엇인가요? 어떤 문제를 해결하나요?
5. Customer Relationships (고객 관계) - 각 고객 세그먼트가 기대하는 관계 유형은 무엇인가요?
6. Channels (채널) - 고객에게 어떻게 도달하고 가치를 전달하나요?
7. Customer Segments (고객 세그먼트) - 가장 중요한 고객은 누구인가요?
8. Cost Structure (비용 구조) - 비즈니스 모델에 내재된 가장 중요한 비용은 무엇인가요?
9. Revenue Streams (수익원) - 고객이 어떤 가치에 대해 비용을 지불하나요? 어떻게 지불하나요?

**중요: 모든 필드의 내용은 반드시 한국어로 작성해야 합니다. 영어를 사용하지 마세요.**"""
        formatted_messages.append(HumanMessage(content=canvas_instruction))
        
        try:
            # Use structured output for Business Model Canvas
            structured_llm = llm.with_structured_output(BusinessModelCanvasData)
            canvas_data = structured_llm.invoke(formatted_messages)
            
            # Convert to JSON string for transmission
            canvas_json = {
                "type": "business_model_canvas",
                "data": canvas_data.model_dump()
            }
            
            return {
                "messages": [AIMessage(content=json.dumps(canvas_json, ensure_ascii=False))],
                "next": "FINISH",
                "last_agent": "framework_designer"
            }
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                error_message = """⚠️ **API 할당량 초과**

현재 Google Gemini API의 무료 티어 할당량을 초과했습니다.

**해결 방법:**
1. 잠시 후 다시 시도해주세요 (약 1분 대기)
2. Google AI Studio에서 할당량 확인: https://ai.dev/usage
3. 필요시 유료 플랜으로 업그레이드 고려

불편을 드려 죄송합니다."""
            else:
                error_message = f"⚠️ **프레임워크 디자이너 오류**\n\n{error_str}\n\n잠시 후 다시 시도해주세요."
            return {
                "messages": [AIMessage(content=error_message)],
                "next": "FINISH",
                "last_agent": "framework_designer"
            }
    
    else:
        # Default: ask which canvas they want
        try:
            response = llm.invoke(formatted_messages + [
                HumanMessage(content=f"{user_message}\n\n어떤 비즈니스 프레임워크를 작성하시겠습니까? 'Lean Canvas' 또는 'Business Model Canvas'를 선택해주세요.")
            ])
            
            return {
                "messages": [AIMessage(content=response.content)],
                "next": "FINISH",
                "last_agent": "framework_designer"
            }
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                error_message = """⚠️ **API 할당량 초과**

현재 Google Gemini API의 무료 티어 할당량을 초과했습니다.

**해결 방법:**
1. 잠시 후 다시 시도해주세요 (약 1분 대기)
2. Google AI Studio에서 할당량 확인: https://ai.dev/usage
3. 필요시 유료 플랜으로 업그레이드 고려

불편을 드려 죄송합니다."""
            else:
                error_message = f"⚠️ **프레임워크 디자이너 오류**\n\n{error_str}\n\n잠시 후 다시 시도해주세요."
            return {
                "messages": [AIMessage(content=error_message)],
                "next": "FINISH",
                "last_agent": "framework_designer"
            }
