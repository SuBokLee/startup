"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "./ui/button"
import { Card } from "./ui/card"
import { Avatar } from "./ui/avatar"
import { Send, Loader2, Moon, Sun } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import LeanCanvas from "./frameworks/LeanCanvas"
import BusinessModelCanvas from "./frameworks/BusinessModelCanvas"
import ConversationHistory from "./ConversationHistory"
import { supabase } from "../lib/supabase"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  agent?: string
  timestamp: Date
}

const AGENT_NAMES: Record<string, string> = {
  cofounder: "Cofounder",
  vc_simulator: "VC Simulator",
  grant_hunter: "Grant Hunter",
  market_sensor: "Market Sensor",
  mvp_builder: "MVP Builder",
  framework_designer: "Framework Designer",
  growth_hacker: "Growth Hacker",
  legal_advisor: "Legal Advisor",
  supervisor: "Master",
}

const AGENT_KEYS = ["cofounder", "vc_simulator", "grant_hunter", "market_sensor", "mvp_builder", "framework_designer", "growth_hacker", "legal_advisor"]

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [isLoadingHistory, setIsLoadingHistory] = useState(false)
  const [refreshHistory, setRefreshHistory] = useState(0)
  const previousConversationIdRef = useRef<string | null>(null)
  const isSendingRef = useRef<boolean>(false)
  const lastMessageRef = useRef<string>("")
  const [isDarkMode, setIsDarkMode] = useState(false)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Apply dark mode to document
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDarkMode])

  // Load conversation when conversationId changes (only if it's a different conversation)
  useEffect(() => {
    if (conversationId && conversationId !== previousConversationIdRef.current) {
      previousConversationIdRef.current = conversationId
      loadConversation(conversationId)
    } else if (!conversationId && previousConversationIdRef.current !== null) {
      // New conversation - show welcome message
      previousConversationIdRef.current = null
      setMessages([
        {
          id: "1",
          role: "assistant",
          content: "안녕하세요! 저는 창업 견인차의 Master입니다. 어떤 도움이 필요하신가요?",
          agent: "supervisor",
          timestamp: new Date(),
        },
      ])
    }
  }, [conversationId])

  const loadConversation = async (convId: string) => {
    try {
      setIsLoadingHistory(true)
      console.log("Loading conversation:", convId)
      const { data: messagesData, error } = await supabase
        .from("messages")
        .select("*")
        .eq("conversation_id", convId)
        .order("created_at", { ascending: true })

      if (error) {
        console.error("Error loading messages:", error)
        throw error
      }

      console.log("Loaded messages:", messagesData?.length || 0)

      if (messagesData && messagesData.length > 0) {
        const loadedMessages: Message[] = messagesData.map((msg) => ({
          id: msg.id,
          role: msg.role as "user" | "assistant",
          content: msg.content,
          agent: msg.agent || undefined,
          timestamp: new Date(msg.created_at),
        }))
        setMessages(loadedMessages)
      } else {
        // No messages found, show welcome message
        setMessages([
          {
            id: "1",
            role: "assistant",
            content: "안녕하세요! 저는 창업 견인차의 Master입니다. 어떤 도움이 필요하신가요?",
            agent: "supervisor",
            timestamp: new Date(),
          },
        ])
      }
    } catch (error) {
      console.error("Error loading conversation:", error)
      // Show error message to user
      setMessages([
        {
          id: "error",
          role: "assistant",
          content: "대화를 불러오는 중 오류가 발생했습니다. 새 대화를 시작해주세요.",
          agent: "supervisor",
          timestamp: new Date(),
        },
      ])
    } finally {
      setIsLoadingHistory(false)
    }
  }

  const createOrUpdateConversation = async (title: string, convId?: string) => {
    try {
      if (convId) {
        // Update existing conversation
        const { error } = await supabase
          .from("conversations")
          .update({ title, updated_at: new Date().toISOString() })
          .eq("id", convId)
        if (error) {
          console.error("Error updating conversation:", error)
          throw error
        }
        console.log("Conversation updated:", convId)
        return convId
      } else {
        // Create new conversation
        const { data, error } = await supabase
          .from("conversations")
          .insert([{ title }])
          .select()
          .single()
        if (error) {
          console.error("Error creating conversation:", error)
          throw error
        }
        console.log("Conversation created:", data.id)
        return data.id
      }
    } catch (error) {
      console.error("Error creating/updating conversation:", error)
      // Return null to indicate failure, but don't block the UI
      return null
    }
  }

  const saveMessage = async (message: Message, convId: string) => {
    try {
      // Check if message already exists to prevent duplicates
      const { data: existingMessages } = await supabase
        .from("messages")
        .select("id")
        .eq("conversation_id", convId)
        .eq("content", message.content)
        .eq("role", message.role)
        .order("created_at", { ascending: false })
        .limit(1)

      if (existingMessages && existingMessages.length > 0) {
        console.log("Message already exists, skipping save:", message.content.substring(0, 50))
        return
      }

      const { error } = await supabase.from("messages").insert([
        {
          conversation_id: convId,
          role: message.role,
          content: message.content,
          agent: message.agent || null,
        },
      ])
      if (error) {
        console.error("Error saving message:", error)
        throw error
      }
      console.log("Message saved successfully:", { convId, role: message.role })
    } catch (error) {
      console.error("Error saving message:", error)
      // Don't throw - allow conversation to continue even if save fails
    }
  }

  const sendMessage = async () => {
    // Prevent duplicate calls
    if (!input.trim() || isLoading || isSendingRef.current) {
      return
    }
    
    // Prevent sending the same message twice
    if (input.trim() === lastMessageRef.current) {
      console.log("Duplicate message prevented:", input.trim())
      return
    }
    
    // Mark as sending
    isSendingRef.current = true
    lastMessageRef.current = input.trim()

    const userMessage: Message = {
      id: `msg_${Date.now()}_${Math.random()}`,
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    // Get or create conversation ID
    let currentConvId = conversationId
    if (!currentConvId) {
      // Create new conversation with first message as title
      const title = input.slice(0, 50) + (input.length > 50 ? "..." : "")
      currentConvId = await createOrUpdateConversation(title)
      if (currentConvId) {
        // Set the ref first to prevent useEffect from triggering
        previousConversationIdRef.current = currentConvId
        setConversationId(currentConvId)
      }
    } else {
      // Update conversation title if this is the first user message
      if (messages.length === 1 && messages[0].role === "assistant") {
        const title = input.slice(0, 50) + (input.length > 50 ? "..." : "")
        await createOrUpdateConversation(title, currentConvId)
      }
    }

    // Add user message to UI immediately (don't reload from DB to avoid duplicates)
    setMessages((prev) => [...prev, userMessage])
    
      // Save user message to database asynchronously (don't block UI)
      if (currentConvId) {
        saveMessage(userMessage, currentConvId).catch((err) => {
          console.error("Error saving user message to database:", err)
          // Don't show error to user, just log it
        })
      }

    const messageToSend = input
    setInput("")
    // Reset textarea height after sending
    setTimeout(() => {
      const textarea = document.querySelector('textarea') as HTMLTextAreaElement
      if (textarea) {
        textarea.style.height = "auto"
        textarea.style.height = "44px"
      }
    }, 100)
    setIsLoading(true)

    try {
      const requestBody: {
        message: string
        thread_id: string
        agent?: string
      } = {
        message: messageToSend,
        thread_id: currentConvId || `thread_${Date.now()}`,
      }
      
      // 선택된 에이전트가 있으면 추가
      if (selectedAgent) {
        requestBody.agent = selectedAgent
      }
      
      // Create abort controller for timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 120000) // 2분 타임아웃
      
      // 환경 변수 확인 (빌드 타임에 주입됨)
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      
      // 환경 변수가 없으면 경고 및 상세 안내
      if (!process.env.NEXT_PUBLIC_API_URL || API_URL === "http://localhost:8000") {
        console.error("❌ NEXT_PUBLIC_API_URL 환경 변수가 설정되지 않았습니다!");
        console.error("❌ 현재 API_URL:", API_URL);
        console.error("❌ 해결 방법:");
        console.error("   1. Vercel → Settings → Environment Variables");
        console.error("   2. NEXT_PUBLIC_API_URL 추가");
        console.error("   3. 값: Railway 백엔드 URL");
        console.error("   4. Preview 환경 체크 필수!");
        console.error("   5. 재배포");
      }
      
      console.log("🔍 API_URL:", API_URL);
      console.log("🔍 Request URL:", `${API_URL}/chat`);
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      })
      
      clearTimeout(timeoutId)

      if (!response.ok) {
        const errorText = await response.text()
        console.error("❌ API Error:", {
          status: response.status,
          statusText: response.statusText,
          url: `${API_URL}/chat`,
          errorText: errorText
        })
        throw new Error(`Server error: ${response.status} - ${errorText}`)
      }

      const data = await response.json()
      
      // 응답 데이터 검증
      if (!data || !data.response) {
        throw new Error("Invalid response format from server")
      }
      
      // 응답에서 받은 agent 이름을 매핑 (백엔드에서 반환하는 형식에 맞춤)
      const agentKey = data.agent || "supervisor"
      let mappedAgent = agentKey
      
      // 백엔드에서 반환하는 agent 이름을 프론트엔드 형식으로 변환
      if (agentKey === "cofounder" || agentKey === "CofounderAgent") {
        mappedAgent = "cofounder"
      } else if (agentKey === "vc_simulator" || agentKey === "VCSimulator") {
        mappedAgent = "vc_simulator"
      } else if (agentKey === "grant_hunter" || agentKey === "GrantHunter") {
        mappedAgent = "grant_hunter"
      } else if (agentKey === "market_sensor" || agentKey === "MarketSensor") {
        mappedAgent = "market_sensor"
      } else if (agentKey === "mvp_builder" || agentKey === "MVPBuilder") {
        mappedAgent = "mvp_builder"
      } else if (agentKey === "framework_designer" || agentKey === "FrameworkDesigner") {
        mappedAgent = "framework_designer"
      } else if (agentKey === "growth_hacker" || agentKey === "GrowthHacker") {
        mappedAgent = "growth_hacker"
      } else if (agentKey === "legal_advisor" || agentKey === "LegalAdvisor") {
        mappedAgent = "legal_advisor"
      } else {
        mappedAgent = "supervisor"
      }

      const assistantMessage: Message = {
        id: `msg_${Date.now()}_${Math.random()}`,
        role: "assistant",
        content: data.response,
        agent: mappedAgent,
        timestamp: new Date(),
      }

      // Add assistant message to UI immediately
      setMessages((prev) => [...prev, assistantMessage])
      
      // Save assistant message to database asynchronously (don't block UI)
      if (currentConvId) {
        saveMessage(assistantMessage, currentConvId).catch((err) => {
          console.error("Error saving message to database:", err)
          // Don't show error to user, just log it
        }).then(() => {
          // Refresh history list after save completes
          setRefreshHistory((prev) => prev + 1)
        })
      }
    } catch (error) {
      console.error("Error sending message:", error)
      
      // 에러 타입에 따라 다른 메시지 표시
      let errorContent = "죄송합니다. 오류가 발생했습니다. 다시 시도해주세요."
      if (error instanceof Error) {
        if (error.name === "AbortError" || error.message.includes("timeout")) {
          errorContent = "요청 시간이 초과되었습니다. 다시 시도해주세요."
        } else if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
          errorContent = "서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요."
        } else {
          errorContent = `오류: ${error.message}`
        }
      }
      
      const errorMessage: Message = {
        id: `msg_${Date.now()}_error`,
        role: "assistant",
        content: errorContent,
        agent: "supervisor",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      // 항상 로딩 상태를 해제하고 입력을 다시 활성화
      setIsLoading(false)
      isSendingRef.current = false
      // Clear last message after a delay to allow same message to be sent again if needed
      setTimeout(() => {
        lastMessageRef.current = ""
      }, 1000)
    }
  }

  const handleSelectConversation = (convId: string) => {
    setConversationId(convId)
  }

  const handleNewConversation = () => {
    setConversationId(null)
    setMessages([
      {
        id: "1",
        role: "assistant",
        content: "안녕하세요! 저는 FounderOS의 Supervisor입니다. 어떤 도움이 필요하신가요?",
        agent: "supervisor",
        timestamp: new Date(),
      },
    ])
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.altKey && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
    // Alt+Enter or Shift+Enter will naturally add a new line in a textarea
  }

  const getAgentDisplayName = (agent?: string) => {
    if (!agent) return "Assistant"
    return AGENT_NAMES[agent] || agent
  }

  return (
    <div className={`flex h-screen ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Sidebar - GPT Style */}
      <div className={`w-64 ${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-gray-50 border-gray-200'} border-r flex flex-col h-screen`}>
        {/* Agent Selection Section - Top */}
        <div className={`p-4 border-b ${isDarkMode ? 'border-gray-700 bg-gray-900' : 'border-gray-200 bg-white'}`}>
          <h2 className={`text-xl font-bold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>창업 견인차</h2>
          <div className={`text-sm font-semibold mb-2 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>에이전트 선택</div>
          <div
            onClick={() => setSelectedAgent(null)}
            className={`p-2 rounded-md text-sm cursor-pointer transition-colors ${
              selectedAgent === null
                ? isDarkMode 
                  ? "bg-blue-900 text-blue-300 font-semibold border-2 border-blue-700"
                  : "bg-blue-100 text-blue-700 font-semibold border-2 border-blue-300"
                : isDarkMode
                  ? "text-gray-300 hover:bg-gray-700"
                  : "text-gray-700 hover:bg-gray-100"
            }`}
          >
            🤖 자동 선택 (Master)
          </div>
          {AGENT_KEYS.map((key) => (
            <div
              key={key}
              onClick={() => setSelectedAgent(key)}
              className={`p-2 rounded-md text-sm cursor-pointer transition-colors ${
                selectedAgent === key
                  ? isDarkMode
                    ? "bg-blue-900 text-blue-300 font-semibold border-2 border-blue-700"
                    : "bg-blue-100 text-blue-700 font-semibold border-2 border-blue-300"
                  : isDarkMode
                    ? "text-gray-300 hover:bg-gray-700"
                    : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {AGENT_NAMES[key]}
            </div>
          ))}
          {selectedAgent && (
            <div className={`mt-2 p-2 rounded-md text-xs ${
              isDarkMode 
                ? "bg-blue-900 text-blue-300"
                : "bg-blue-50 text-blue-600"
            }`}>
              선택됨: {AGENT_NAMES[selectedAgent]}
            </div>
          )}
        </div>
        
        {/* Conversation History - Bottom */}
        <ConversationHistory
          onSelectConversation={handleSelectConversation}
          currentConversationId={conversationId}
          onNewConversation={handleNewConversation}
          refreshTrigger={refreshHistory}
          isDarkMode={isDarkMode}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className={`${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b p-4 flex items-center justify-between`}>
          <div>
            <h1 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>창업 견인차</h1>
            <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>스타트업 창업자를 위한 AI 어시스턴트</p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="ml-4"
          >
            {isDarkMode ? (
              <Sun className="h-5 w-5 text-yellow-500" />
            ) : (
              <Moon className="h-5 w-5 text-gray-600" />
            )}
          </Button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {isLoadingHistory ? (
            <div className="flex justify-center items-center h-full">
              <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
              {message.role === "assistant" && (
                <Avatar
                  variant={message.agent === "supervisor" ? "supervisor" : "agent"}
                  agentName={getAgentDisplayName(message.agent)}
                />
              )}
              <Card className={`max-w-2xl ${
                message.role === "user"
                  ? isDarkMode 
                    ? "bg-blue-700 text-white"
                    : "bg-blue-600 text-white"
                  : isDarkMode
                    ? "bg-gray-800 text-gray-100"
                    : "bg-white"
              }`}>
                <div className={`p-4 ${(() => {
                  // Check if content is structured JSON for canvas
                  try {
                    const parsed = JSON.parse(message.content)
                    if ((parsed.type === "lean_canvas" || parsed.type === "business_model_canvas") && parsed.data) {
                      return "p-0" // Remove padding for canvas
                    }
                  } catch (e) {
                    // Not JSON
                  }
                  return ""
                })()}`}>
                  {message.role === "assistant" && message.agent && (
                    <div className={`text-xs font-semibold mb-2 px-4 pt-4 ${
                      message.agent === "supervisor"
                        ? isDarkMode ? "text-purple-400" : "text-purple-600"
                        : isDarkMode ? "text-green-400" : "text-green-600"
                    }`}>
                      {getAgentDisplayName(message.agent)}
                    </div>
                  )}
                  {message.role === "assistant" ? (
                    (() => {
                      // Check if content is structured JSON for canvas
                      try {
                        const parsed = JSON.parse(message.content)
                        if (parsed.type === "lean_canvas" && parsed.data) {
                          return (
                            <div className="px-4 pb-4">
                              <LeanCanvas data={parsed.data} />
                            </div>
                          )
                        } else if (parsed.type === "business_model_canvas" && parsed.data) {
                          return (
                            <div className="px-4 pb-4">
                              <BusinessModelCanvas data={parsed.data} />
                            </div>
                          )
                        }
                      } catch (e) {
                        // Not JSON, render as markdown
                      }
                      
                      // Render as markdown
                      return (
                        <div className={`prose prose-sm max-w-none ${isDarkMode ? 'prose-invert' : ''}`}>
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              code: ({ node, inline, className, children, ...props }: any) => {
                                const match = /language-(\w+)/.exec(className || "")
                                return !inline && match ? (
                                  <div className="relative">
                                    <div className={`absolute top-2 right-2 text-xs ${isDarkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                                      {match[1]}
                                    </div>
                                    <pre className={`${isDarkMode ? 'bg-gray-950 text-gray-100' : 'bg-gray-900 text-gray-100'} p-4 rounded-lg overflow-x-auto mb-4 mt-2`}>
                                      <code className={className} {...props}>
                                        {children}
                                      </code>
                                    </pre>
                                  </div>
                                ) : (
                                  <code className={`${isDarkMode ? 'bg-gray-700 text-gray-200' : 'bg-gray-100 text-gray-800'} px-1.5 py-0.5 rounded text-sm font-mono`} {...props}>
                                    {children}
                                  </code>
                                )
                              },
                              pre: ({ children }: any) => <>{children}</>,
                              p: ({ children }: any) => <p className={`mb-2 last:mb-0 ${isDarkMode ? 'text-gray-200' : ''}`}>{children}</p>,
                              ul: ({ children }: any) => <ul className={`list-disc list-inside mb-2 space-y-1 ${isDarkMode ? 'text-gray-200' : ''}`}>{children}</ul>,
                              ol: ({ children }: any) => <ol className={`list-decimal list-inside mb-2 space-y-1 ${isDarkMode ? 'text-gray-200' : ''}`}>{children}</ol>,
                              li: ({ children }: any) => <li className={`ml-4 ${isDarkMode ? 'text-gray-200' : ''}`}>{children}</li>,
                              h1: ({ children }: any) => <h1 className={`text-2xl font-bold mb-2 mt-4 ${isDarkMode ? 'text-white' : ''}`}>{children}</h1>,
                              h2: ({ children }: any) => <h2 className={`text-xl font-bold mb-2 mt-3 ${isDarkMode ? 'text-white' : ''}`}>{children}</h2>,
                              h3: ({ children }: any) => <h3 className={`text-lg font-bold mb-2 mt-2 ${isDarkMode ? 'text-white' : ''}`}>{children}</h3>,
                              blockquote: ({ children }: any) => (
                                <blockquote className={`border-l-4 pl-4 italic my-2 ${isDarkMode ? 'border-gray-600 text-gray-300' : 'border-gray-300'}`}>
                                  {children}
                                </blockquote>
                              ),
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      )
                    })()
                  ) : (
                    <div className="whitespace-pre-wrap text-white">
                      {message.content}
                    </div>
                  )}
                  <div className={`text-xs mt-2 ${
                    message.role === "user" ? "text-blue-100" : "text-gray-500"
                  }`}>
                    {message.timestamp.toLocaleTimeString("ko-KR", {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>
                </div>
              </Card>
              {message.role === "user" && (
                <Avatar variant="user" />
              )}
            </div>
            ))
          )}
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <Avatar variant="supervisor" />
              <Card className={isDarkMode ? "bg-gray-800" : "bg-white"}>
                <div className="p-4">
                  <Loader2 className={`h-5 w-5 animate-spin ${isDarkMode ? 'text-gray-300' : 'text-gray-400'}`} />
                </div>
              </Card>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className={`${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-t p-4`}>
          <div className="flex gap-2 max-w-4xl mx-auto">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="메시지를 입력하세요... (Enter: 전송, Shift+Enter 또는 Alt+Enter: 줄바꿈)"
              disabled={isLoading}
              className={`flex-1 min-h-[44px] max-h-[200px] resize-none rounded-md border px-3 py-2 text-sm placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${
                isDarkMode
                  ? 'border-gray-600 bg-gray-700 text-white placeholder:text-gray-400'
                  : 'border-gray-300 bg-white text-black'
              }`}
              rows={1}
              style={{
                height: "auto",
                minHeight: "44px",
              }}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement
                target.style.height = "auto"
                target.style.height = `${Math.min(target.scrollHeight, 200)}px`
              }}
            />
            <Button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              size="default"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

