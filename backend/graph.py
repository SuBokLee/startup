"""
LangGraph implementation for FounderOS Supervisor and Agent routing
"""

from typing import Dict, Any, Literal
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm import get_supervisor_llm
from state import AgentState
from agents.cofounder import cofounder_node
from agents.grant_hunter import grant_hunter_node
from agents.market_sensor import market_sensor_node
from agents.vc_simulator import vc_simulator_node
from agents.mvp_builder import mvp_builder_node
from agents.framework_designer import framework_designer_node
from agents.growth_hacker import growth_hacker_node
from agents.legal_advisor import legal_advisor_node


# Define the routing decision structure
class RoutingDecision(BaseModel):
    """Structured output for supervisor routing"""
    next_agent: Literal[
        "CofounderAgent",
        "VCSimulator", 
        "GrantHunter",
        "MarketSensor",
        "MVPBuilder",
        "FrameworkDesigner",
        "GrowthHacker",
        "LegalAdvisor",
        "FINISH"
    ] = Field(
        description="The name of the next agent to execute, or 'FINISH' if the task is complete"
    )


# Agent members
AGENT_MEMBERS = [
    "CofounderAgent",
    "VCSimulator",
    "GrantHunter", 
    "MarketSensor",
    "MVPBuilder",
    "FrameworkDesigner",
    "GrowthHacker",
    "LegalAdvisor"
]


def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    Supervisor node that routes to the appropriate agent
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with routing decision
    """
    llm = get_supervisor_llm()
    
    messages = state.get("messages", [])
    if not messages:
        return {"next": END}
    
    # Check if the last message is from AI - if so, wait for user input (FINISH)
    last_message = messages[-1]
    if isinstance(last_message, AIMessage):
        # AI just responded, wait for next user message
        return {"next": END, "last_agent": state.get("last_agent", "")}
    
    # Get the last user message (skip AI messages)
    user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
    if not user_messages:
        return {"next": END}
    
    user_message = user_messages[-1].content if hasattr(user_messages[-1], 'content') else str(user_messages[-1])
    
    # Create supervisor prompt
    # Get conversation history for context
    conversation_context = ""
    if len(messages) > 1:
        recent_messages = messages[-3:]  # Last 3 messages for context
        conversation_context = "\n\nRecent conversation:\n"
        for msg in recent_messages:
            if isinstance(msg, HumanMessage):
                conversation_context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                conversation_context += f"Assistant: {msg.content}\n"
    
    supervisor_prompt = f"""You are the supervisor (마스터) managing a conversation between worker agents: {', '.join(AGENT_MEMBERS)}.

Given the user request, you MUST route to the appropriate agent. Only respond with 'FINISH' if the task is truly complete or if you need to wait for more user input.

Available agents and their purposes:
- CofounderAgent: 비즈니스 전략, 비즈니스 모델 논의, 멘탈 지원, 논리적 토론, 창업 아이디어 검토, 일반적인 창업 조언
- VCSimulator: 피치덱 리뷰, 투자자 질문, 펀드레이징 준비, 투자 유치 상담, VC 피칭, 투자자 관점의 피드백
- GrantHunter: 정부 보조금 검색, 보조금 신청, 자금 조달 기회, K-Startup 프로그램, 정부 지원사업, 지원금
- MarketSensor: 경쟁사 분석, 시장 트렌드, 감정 분석, 산업 인텔리전스, 시장 조사, 경쟁 분석, 시장 규모
- MVPBuilder: PRD 생성, 코딩 작업, 랜딩 페이지, 프로토타이핑, 개발, 코드 작성, 기술 구현
- FrameworkDesigner: 구조화된 비즈니스 프레임워크 생성 (Lean Canvas, Business Model Canvas), 캔버스 작성
- GrowthHacker: 마케팅 콘텐츠 작성, 콜드 이메일, 소셜 미디어 포스트, 블로그 글, SEO 최적화, 성장 마케팅
- LegalAdvisor: 계약서 작성, 법률 검토, NDA, MOU, 서비스 계약서, 고용 계약서, 법률 조항 분석, 법률 자문

Current user request: {user_message}
{conversation_context}

CRITICAL ROUTING RULES - Analyze the user's request and route to the MOST APPROPRIATE agent:
1. If the user asks about 보조금, 지원사업, 정부 프로그램, K-Startup, 자금조달, 지원금 → GrantHunter
2. If the user asks about 경쟁사, 시장, 트렌드, 경쟁력, 시장분석, 경쟁분석, 시장규모 → MarketSensor
3. If the user asks about 코드, 개발, MVP, 프로토타입, PRD, 프로그래밍, 기술, 구현, 만들기 → MVPBuilder
4. If the user asks about 투자, VC, 피치, 펀드레이징, 투자유치, 투자자, 피치덱 → VCSimulator
5. If the user asks about 캔버스, Lean Canvas, BMC, 비즈니스모델캔버스, 린캔버스 → FrameworkDesigner
6. If the user asks about 마케팅, 홍보, 콘텐츠 작성, 콜드 이메일, 소셜미디어, 블로그, SEO, 성장, 마케팅 글 → GrowthHacker
7. If the user asks about 계약서, 법률, NDA, 비밀유지서약서, 법률 검토, 변호사, 조항, 합의서, 계약, 법률 자문 → LegalAdvisor
8. If the user asks about 비즈니스 전략, 아이디어, 모델, 창업 조언, 일반적인 질문 → CofounderAgent

You MUST respond with ONLY the agent name (e.g., "GrantHunter", "MarketSensor", etc.) or "FINISH" if the conversation is complete.

Determine which agent should handle this request NOW and respond with that agent's name."""
    
    try:
        # Use structured output for routing
        structured_llm = llm.with_structured_output(RoutingDecision)
        decision = structured_llm.invoke([HumanMessage(content=supervisor_prompt)])
        
        next_agent = decision.next_agent
        
        # Map agent names to node names
        agent_to_node = {
            "CofounderAgent": "cofounder",
            "VCSimulator": "vc_simulator",
            "GrantHunter": "grant_hunter",
            "MarketSensor": "market_sensor",
            "MVPBuilder": "mvp_builder",
            "FrameworkDesigner": "framework_designer",
            "GrowthHacker": "growth_hacker",
            "LegalAdvisor": "legal_advisor",
            "FINISH": END
        }
        
        return {"next": agent_to_node.get(next_agent, END)}
    
    except Exception as e:
        print(f"Supervisor routing error: {e}, using keyword fallback")
        # Fallback: try to route based on keywords (Korean and English)
        user_message_lower = user_message.lower()
        
        # Priority order matters - check more specific first
        if any(keyword in user_message_lower for keyword in ["lean canvas", "business model canvas", "bmc", "캔버스", "린캔버스", "비즈니스모델캔버스", "비즈니스 모델 캔버스"]):
            print(f"Fallback routing: framework_designer for message: {user_message[:50]}")
            return {"next": "framework_designer"}
        elif any(keyword in user_message_lower for keyword in ["보조금", "지원사업", "k-startup", "k startup", "정부", "지원", "grant", "government", "funding", "자금조달", "지원금"]):
            print(f"Fallback routing: grant_hunter for message: {user_message[:50]}")
            return {"next": "grant_hunter"}
        elif any(keyword in user_message_lower for keyword in ["경쟁사", "시장", "트렌드", "경쟁력", "시장분석", "market", "competitor", "trend", "analysis", "경쟁", "시장규모"]):
            print(f"Fallback routing: market_sensor for message: {user_message[:50]}")
            return {"next": "market_sensor"}
        elif any(keyword in user_message_lower for keyword in ["코드", "개발", "mvp", "prd", "프로토타입", "프로그래밍", "code", "build", "prototype", "programming", "개발해", "만들어", "기술", "구현"]):
            print(f"Fallback routing: mvp_builder for message: {user_message[:50]}")
            return {"next": "mvp_builder"}
        elif any(keyword in user_message_lower for keyword in ["투자", "vc", "벤처캐피털", "피치", "펀드레이징", "investor", "pitch", "fundraising", "투자유치", "피치덱"]):
            print(f"Fallback routing: vc_simulator for message: {user_message[:50]}")
            return {"next": "vc_simulator"}
        elif any(keyword in user_message_lower for keyword in ["마케팅", "홍보", "콘텐츠", "콜드 이메일", "소셜미디어", "소셜 미디어", "블로그", "seo", "성장", "마케팅 글", "포스트", "이메일 작성", "marketing", "growth", "content", "email"]):
            print(f"Fallback routing: growth_hacker for message: {user_message[:50]}")
            return {"next": "growth_hacker"}
        elif any(keyword in user_message_lower for keyword in ["계약서", "법률", "nda", "비밀유지서약서", "법률 검토", "변호사", "조항", "합의서", "계약", "법률 자문", "contract", "legal", "lawyer", "clause", "agreement", "mou"]):
            print(f"Fallback routing: legal_advisor for message: {user_message[:50]}")
            return {"next": "legal_advisor"}
        elif any(keyword in user_message_lower for keyword in ["비즈니스", "전략", "모델", "아이디어", "창업", "business", "strategy", "cofounder", "idea", "startup"]):
            print(f"Fallback routing: cofounder for message: {user_message[:50]}")
            return {"next": "cofounder"}
        else:
            # Default to cofounder for general queries
            print(f"Defaulting to cofounder for message: {user_message[:50]}")
            return {"next": "cofounder"}


def route_decision(state: AgentState):
    """
    Route to the next node based on supervisor decision
    
    Args:
        state: Current agent state
    
    Returns:
        Next node name or END
    """
    next_node = state.get("next", END)
    # Ensure we only return valid nodes
    if next_node == "cofounder":
        return "cofounder"
    elif next_node == "vc_simulator":
        return "vc_simulator"
    elif next_node == "grant_hunter":
        return "grant_hunter"
    elif next_node == "market_sensor":
        return "market_sensor"
    elif next_node == "mvp_builder":
        return "mvp_builder"
    elif next_node == "framework_designer":
        return "framework_designer"
    elif next_node == "growth_hacker":
        return "growth_hacker"
    elif next_node == "legal_advisor":
        return "legal_advisor"
    elif next_node == END or next_node == "FINISH":
        return END
    else:
        return END


def build_graph():
    """
    Build and compile the LangGraph
    
    Returns:
        Compiled LangGraph
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("cofounder", cofounder_node)
    workflow.add_node("vc_simulator", vc_simulator_node)
    workflow.add_node("grant_hunter", grant_hunter_node)
    workflow.add_node("market_sensor", market_sensor_node)
    workflow.add_node("mvp_builder", mvp_builder_node)
    workflow.add_node("framework_designer", framework_designer_node)
    workflow.add_node("growth_hacker", growth_hacker_node)
    workflow.add_node("legal_advisor", legal_advisor_node)
    
    # Set entry point
    workflow.set_entry_point("supervisor")
    
    # Add conditional edge from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_decision,
        {
            "cofounder": "cofounder",
            "vc_simulator": "vc_simulator",
            "grant_hunter": "grant_hunter",
            "market_sensor": "market_sensor",
            "mvp_builder": "mvp_builder",
            "framework_designer": "framework_designer",
            "growth_hacker": "growth_hacker",
            "legal_advisor": "legal_advisor",
            END: END
        }
    )
    
    # All agents finish after responding (wait for next user message)
    workflow.add_edge("cofounder", END)
    workflow.add_edge("vc_simulator", END)
    workflow.add_edge("grant_hunter", END)
    workflow.add_edge("market_sensor", END)
    workflow.add_edge("mvp_builder", END)
    workflow.add_edge("framework_designer", END)
    workflow.add_edge("growth_hacker", END)
    workflow.add_edge("legal_advisor", END)
    workflow.add_edge("legal_advisor", END)
    
    # Return workflow (not compiled yet, will be compiled with checkpointer in main.py)
    return workflow


# Create graph workflow (will be compiled with checkpointer in main.py)
graph_workflow = build_graph()

