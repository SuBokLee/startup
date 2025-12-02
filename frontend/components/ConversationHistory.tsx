"use client"

import { useState, useEffect } from "react"
import { Button } from "./ui/button"
import { supabase, Conversation } from "../lib/supabase"
import { Trash2 } from "lucide-react"

interface ConversationHistoryProps {
  onSelectConversation: (conversationId: string) => void
  currentConversationId: string | null
  onNewConversation: () => void
  refreshTrigger?: number // Add refresh trigger
  isDarkMode?: boolean
}

export default function ConversationHistory({
  onSelectConversation,
  currentConversationId,
  onNewConversation,
  refreshTrigger,
  isDarkMode = false,
}: ConversationHistoryProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadConversations()
  }, [refreshTrigger])

  const loadConversations = async () => {
    try {
      setIsLoading(true)
      console.log("Loading conversations...")
      const { data, error } = await supabase
        .from("conversations")
        .select("*")
        .order("updated_at", { ascending: false })
        .limit(20)

      if (error) {
        console.error("Error loading conversations:", error)
        throw error
      }
      console.log("Loaded conversations:", data?.length || 0)
      setConversations(data || [])
    } catch (error) {
      console.error("Error loading conversations:", error)
      // Show error to user
      alert("대화 기록을 불러오는 중 오류가 발생했습니다. 콘솔을 확인해주세요.")
    } finally {
      setIsLoading(false)
    }
  }

  const deleteConversation = async (id: string) => {
    try {
      const { error } = await supabase
        .from("conversations")
        .delete()
        .eq("id", id)

      if (error) throw error
      await loadConversations()
      if (currentConversationId === id) {
        onNewConversation()
      }
    } catch (error) {
      console.error("Error deleting conversation:", error)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (days === 0) {
      return date.toLocaleTimeString("ko-KR", {
        hour: "2-digit",
        minute: "2-digit",
      })
    } else if (days === 1) {
      return "어제"
    } else if (days < 7) {
      return `${days}일 전`
    } else {
      return date.toLocaleDateString("ko-KR", {
        month: "short",
        day: "numeric",
      })
    }
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      {/* Header */}
      <div className={`p-4 border-b ${isDarkMode ? 'border-gray-700 bg-gray-900' : 'border-gray-200 bg-white'}`}>
        <Button
          onClick={() => {
            onNewConversation()
          }}
          className="w-full"
          size="sm"
        >
          + 새 대화
        </Button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className={`text-center py-4 px-4 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>로딩 중...</div>
        ) : conversations.length === 0 ? (
          <div className={`text-center py-4 px-4 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            <div className="text-sm">대화 기록이 없습니다</div>
            <div className="text-xs mt-2">새 대화를 시작해보세요</div>
          </div>
        ) : (
          <div className="py-2">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                className={`group relative px-3 py-2.5 mx-2 mb-1 rounded-lg cursor-pointer transition-colors ${
                  currentConversationId === conv.id
                    ? isDarkMode ? "bg-gray-700" : "bg-gray-200"
                    : isDarkMode ? "hover:bg-gray-700" : "hover:bg-gray-100"
                }`}
                onClick={() => {
                  onSelectConversation(conv.id)
                }}
              >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0 pr-8">
                      <div className={`font-medium text-sm truncate ${
                        isDarkMode ? 'text-gray-200' : 'text-gray-800'
                      }`}>
                        {conv.title}
                      </div>
                      <div className={`text-xs mt-1 ${
                        isDarkMode ? 'text-gray-400' : 'text-gray-500'
                      }`}>
                        {formatDate(conv.updated_at)}
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 h-6 w-6 p-0 transition-opacity"
                      onClick={(e) => {
                        e.stopPropagation()
                        if (confirm("이 대화를 삭제하시겠습니까?")) {
                          deleteConversation(conv.id)
                        }
                      }}
                    >
                      <Trash2 className={`h-3 w-3 ${isDarkMode ? 'text-gray-400 hover:text-red-400' : 'text-gray-500 hover:text-red-500'}`} />
                    </Button>
                  </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

