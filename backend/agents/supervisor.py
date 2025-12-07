"""
Supervisor Agent using LangGraph for routing
"""

from typing import Dict, Any, Literal, TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import operator

from .cofounder import CofounderAgent
from .vc_coach import VCCoachAgent
from .grant_hunter import GrantHunterAgent
from .market_sensor import MarketSensorAgent
from .mvp_builder import MVPBuilderAgent
from prompts import SUPERVISOR_PROMPT


class GraphState(TypedDict):
    """State for the LangGraph supervisor"""
    messages: Annotated[list, add_messages]
    current_agent: str
    output: str
    routing_decision: str


class SupervisorAgent:
    """Supervisor Agent that routes requests to specialist agents"""
    
    def __init__(self):
        # Use gemini-1.5-flash-latest for better quota limits and compatibility
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)
        
        # Initialize specialist agents
        self.agents = {
            "cofounder": CofounderAgent(),
            "vc_coach": VCCoachAgent(),
            "grant_hunter": GrantHunterAgent(),
            "market_sensor": MarketSensorAgent(),
            "mvp_builder": MVPBuilderAgent(),
        }
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph supervisor graph"""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("cofounder", self._cofounder_node)
        workflow.add_node("vc_coach", self._vc_coach_node)
        workflow.add_node("grant_hunter", self._grant_hunter_node)
        workflow.add_node("market_sensor", self._market_sensor_node)
        workflow.add_node("mvp_builder", self._mvp_builder_node)
        
        # Set entry point
        workflow.set_entry_point("supervisor")
        
        # Add conditional edges from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            self._route_decision,
            {
                "cofounder": "cofounder",
                "vc_coach": "vc_coach",
                "grant_hunter": "grant_hunter",
                "market_sensor": "market_sensor",
                "mvp_builder": "mvp_builder",
                "end": END,
            }
        )
        
        # All agent nodes end after processing
        workflow.add_edge("cofounder", END)
        workflow.add_edge("vc_coach", END)
        workflow.add_edge("grant_hunter", END)
        workflow.add_edge("market_sensor", END)
        workflow.add_edge("mvp_builder", END)
        
        return workflow.compile()
    
    async def _supervisor_node(self, state: GraphState) -> Dict[str, Any]:
        """Supervisor node that decides routing"""
        messages = state.get("messages", [])
        
        # If we already have output, we're done
        if state.get("output"):
            return {
                "routing_decision": "end"
            }
        
        if not messages:
            return {
                "routing_decision": "end",
                "output": "No messages to process."
            }
        
        # Get the last user message
        last_message = messages[-1]
        user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        try:
            from langchain.schema import SystemMessage, HumanMessage
            messages = [
                SystemMessage(content=SUPERVISOR_PROMPT),
                HumanMessage(content=user_message)
            ]
            response = await self.llm.ainvoke(messages)
            
            decision = response.content.lower().strip()
            
            # Map to valid agent names
            agent_mapping = {
                "cofounder": "cofounder",
                "virtual co-founder": "cofounder",
                "virtual cofounder": "cofounder",
                "co-founder": "cofounder",
                "vc": "vc_coach",
                "vc coach": "vc_coach",
                "vc simulator": "vc_coach",
                "grant": "grant_hunter",
                "grant hunter": "grant_hunter",
                "market": "market_sensor",
                "market sensor": "market_sensor",
                "mvp": "mvp_builder",
                "mvp builder": "mvp_builder",
                "prd": "mvp_builder",
                "code": "mvp_builder",
                "prototype": "mvp_builder",
            }
            
            # Try to find matching agent
            routing_decision = "end"
            for key, agent in agent_mapping.items():
                if key in decision:
                    routing_decision = agent
                    break
            
            # If no match, try direct match
            if routing_decision == "end" and decision in self.agents:
                routing_decision = decision
            
            # If still no match, default to cofounder for general queries
            if routing_decision == "end":
                routing_decision = "cofounder"
            
            return {
                "routing_decision": routing_decision,
                "current_agent": routing_decision
            }
        except Exception as e:
            return {
                "routing_decision": "end",
                "output": f"Supervisor error: {str(e)}"
            }
    
    def _route_decision(self, state: GraphState) -> str:
        """Determine next node based on routing decision"""
        decision = state.get("routing_decision", "end")
        return decision if decision in ["cofounder", "vc_coach", "grant_hunter", "market_sensor", "mvp_builder", "end"] else "end"
    
    async def _cofounder_node(self, state: GraphState) -> Dict[str, Any]:
        """Process through cofounder agent"""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message:
            return {"output": "No message to process"}
        
        user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Get conversation history
        history = []
        for msg in messages[:-1]:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        response = await self.agents["cofounder"].process(user_message, {"history": history})
        
        return {
            "output": response,
            "messages": [AIMessage(content=response)]
        }
    
    async def _vc_coach_node(self, state: GraphState) -> Dict[str, Any]:
        """Process through VC coach agent"""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message:
            return {"output": "No message to process"}
        
        user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        history = []
        for msg in messages[:-1]:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        response = await self.agents["vc_coach"].process(user_message, {"history": history})
        
        return {
            "output": response,
            "messages": [AIMessage(content=response)]
        }
    
    async def _grant_hunter_node(self, state: GraphState) -> Dict[str, Any]:
        """Process through grant hunter agent"""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message:
            return {"output": "No message to process"}
        
        user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        history = []
        for msg in messages[:-1]:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        response = await self.agents["grant_hunter"].process(user_message, {"history": history})
        
        return {
            "output": response,
            "messages": [AIMessage(content=response)]
        }
    
    async def _market_sensor_node(self, state: GraphState) -> Dict[str, Any]:
        """Process through market sensor agent"""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message:
            return {"output": "No message to process"}
        
        user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        history = []
        for msg in messages[:-1]:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        response = await self.agents["market_sensor"].process(user_message, {"history": history})
        
        return {
            "output": response,
            "messages": [AIMessage(content=response)]
        }
    
    async def _mvp_builder_node(self, state: GraphState) -> Dict[str, Any]:
        """Process through MVP builder agent"""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message:
            return {"output": "No message to process"}
        
        user_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        history = []
        for msg in messages[:-1]:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        response = await self.agents["mvp_builder"].process(user_message, {"history": history})
        
        return {
            "output": response,
            "messages": [AIMessage(content=response)]
        }
    
    async def process(self, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """Process a user message through the supervisor graph"""
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "current_agent": "supervisor",
            "output": "",
            "routing_decision": ""
        }
        
        try:
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            
            return {
                "response": final_state.get("output", "No response generated"),
                "agent": final_state.get("current_agent", "supervisor"),
                "routing_decision": final_state.get("routing_decision", "")
            }
        except Exception as e:
            return {
                "response": f"Error processing message: {str(e)}",
                "agent": "supervisor",
                "routing_decision": "error"
            }

