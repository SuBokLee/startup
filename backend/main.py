"""
Startup Sherpa Backend - FastAPI Application with LangGraph
창업을 도와주는 짐꾼이자 길잡이
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from graph import graph_workflow
from direct_agent import route_to_agent

# Load environment variables
load_dotenv()

app = FastAPI(title="Startup Sherpa API", version="2.0.0")

# CORS middleware
# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize memory for conversation context
memory = MemorySaver()

# Compile graph with memory checkpointer
graph_with_memory = graph_workflow.compile(checkpointer=memory)


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str
    thread_id: Optional[str] = None
    agent: Optional[str] = None  # 선택된 에이전트 (선택사항)


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    agent: str
    thread_id: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Startup Sherpa API - 창업을 도와주는 짐꾼이자 길잡이",
        "version": "2.0.0",
        "agents": [
            "CofounderAgent",
            "VCSimulator",
            "GrantHunter",
            "MarketSensor",
            "MVPBuilder"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    REST API endpoint for chat with conversation context
    
    Args:
        chat_message: Chat message with optional thread_id
    
    Returns:
        Chat response with agent name and thread_id
    """
    try:
        # Generate or use thread_id
        thread_id = chat_message.thread_id or f"thread_{os.urandom(8).hex()}"
        
        # If agent is specified, route directly to that agent
        if chat_message.agent and chat_message.agent != "supervisor" and chat_message.agent != "":
            result = await route_to_agent(
                agent_name=chat_message.agent,
                message=chat_message.message,
                thread_id=thread_id,
                graph_with_memory=graph_with_memory
            )
            return ChatResponse(
                response=result["response"],
                agent=result["agent"],
                thread_id=result["thread_id"]
            )
        
        # Otherwise, use supervisor routing
        # Create config for this thread with recursion limit
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50  # Increase recursion limit
        }
        
        # Invoke graph with user message
        result = await graph_with_memory.ainvoke(
            {"messages": [HumanMessage(content=chat_message.message)]},
            config=config
        )
        
        # Get the last AI message
        messages = result.get("messages", [])
        last_message = messages[-1] if messages else None
        
        response_text = last_message.content if last_message else "No response generated"
        
        # Determine which agent responded from state
        agent = result.get("last_agent", "supervisor")
        
        # Map agent node names to frontend-friendly names
        agent_name_mapping = {
            "cofounder": "cofounder",
            "vc_simulator": "vc_simulator",
            "grant_hunter": "grant_hunter",
            "market_sensor": "market_sensor",
            "mvp_builder": "mvp_builder",
            "framework_designer": "framework_designer",
            "growth_hacker": "growth_hacker",
            "legal_advisor": "legal_advisor",
        }
        
        # Use mapped name or default to supervisor
        mapped_agent = agent_name_mapping.get(agent, "supervisor")
        
        return ChatResponse(
            response=response_text,
            agent=mapped_agent,
            thread_id=thread_id
        )
    
    except Exception as e:
        error_str = str(e)
        
        # Handle quota exceeded errors
        if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
            error_message = """⚠️ **API 할당량 초과**

현재 Google Gemini API의 무료 티어 할당량을 초과했습니다.

**해결 방법:**
1. 잠시 후 다시 시도해주세요 (약 1분 대기)
2. Google AI Studio에서 할당량 확인: https://ai.dev/usage
3. 필요시 유료 플랜으로 업그레이드 고려

**대안:**
- 다른 에이전트를 사용해보세요
- 잠시 후 다시 시도해주세요

불편을 드려 죄송합니다."""
        elif "Error" in error_str or "error" in error_str.lower():
            error_message = f"⚠️ **오류가 발생했습니다**\n\n{error_str}\n\n잠시 후 다시 시도해주세요."
        else:
            error_message = f"⚠️ **오류가 발생했습니다**\n\n{error_str}"
        
        return ChatResponse(
            response=error_message,
            agent="supervisor",
            thread_id=chat_message.thread_id or "error"
        )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket.accept()
    
    # Store thread_id for this connection
    thread_id = None
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            thread_id = message_data.get("thread_id") or thread_id or f"thread_{os.urandom(8).hex()}"
            selected_agent = message_data.get("agent")
            
            if not user_message:
                await websocket.send_json({
                    "response": "Please provide a message",
                    "agent": "supervisor",
                    "thread_id": thread_id
                })
                continue
            
            # If agent is specified, route directly to that agent
            if selected_agent and selected_agent != "supervisor":
                result = await route_to_agent(
                    agent_name=selected_agent,
                    message=user_message,
                    thread_id=thread_id,
                    graph_with_memory=graph_with_memory
                )
                await websocket.send_json({
                    "response": result["response"],
                    "agent": result["agent"],
                    "thread_id": result["thread_id"]
                })
                continue
            
            # Otherwise, use supervisor routing
            # Create config for this thread with recursion limit
            config = {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 50  # Increase recursion limit
            }
            
            # Invoke graph
            result = await graph_with_memory.ainvoke(
                {"messages": [HumanMessage(content=user_message)]},
                config=config
            )
            
            # Get the last AI message
            messages = result.get("messages", [])
            last_message = messages[-1] if messages else None
            
            response_text = last_message.content if last_message else "No response generated"
            
            # Send response
            await websocket.send_json({
                "response": response_text,
                "agent": "supervisor",
                "thread_id": thread_id
            })
    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({
            "response": f"Error: {str(e)}",
            "agent": "supervisor",
            "thread_id": thread_id or "error"
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
