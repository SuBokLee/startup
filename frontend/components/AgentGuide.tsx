"use client"

import { HelpCircle } from "lucide-react"
import { useState } from "react"

interface AgentInfo {
  icon: string
  name: string
  description: string
}

const AGENTS: AgentInfo[] = [
  {
    icon: "🤝",
    name: "공동 창업자 (Co-founder)",
    description: "아이디어 고도화, 논리적 토론 및 멘탈 케어"
  },
  {
    icon: "💰",
    name: "지원사업 알리미 (Grant Hunter)",
    description: "내게 맞는 정부 지원사업(K-Startup) 실시간 검색"
  },
  {
    icon: "📡",
    name: "시장 조사관 (Market Sensor)",
    description: "경쟁사 분석, 시장 트렌드 및 소비자 반응 파악"
  },
  {
    icon: "📐",
    name: "프레임워크 디자이너",
    description: "비즈니스 모델 캔버스(BMC) & 린 캔버스 시각화"
  },
  {
    icon: "💸",
    name: "투자자 시뮬레이터 (VC)",
    description: "사업계획서 검토, 팩트 폭격 및 투자 유치 전략 조언"
  },
  {
    icon: "💻",
    name: "MVP 빌더 (Developer)",
    description: "웹사이트 랜딩 페이지 및 주요 기능 코드(React) 생성"
  },
  {
    icon: "⚖️",
    name: "법률 자문 (Legal Advisor)",
    description: "NDA, 용역 계약서 등 표준 계약서 작성 및 독소 조항 검토"
  },
  {
    icon: "🚀",
    name: "그로스 해커 (Marketer)",
    description: "바이럴 마케팅 카피라이팅, 블로그 글 및 콜드 메일 작성"
  }
]

interface AgentGuideProps {
  isDarkMode?: boolean
}

export default function AgentGuide({ isDarkMode = false }: AgentGuideProps) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div className="relative">
      <button
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={`p-2 rounded-lg transition-colors ${
          isDarkMode
            ? "hover:bg-gray-700 text-gray-300"
            : "hover:bg-gray-100 text-gray-600"
        }`}
        aria-label="에이전트 가이드"
      >
        <HelpCircle className="w-5 h-5" />
      </button>

      {/* Hover Card */}
      {isHovered && (
        <div
          className={`absolute right-0 top-full mt-2 w-[400px] rounded-lg shadow-lg border z-50 ${
            isDarkMode
              ? "bg-gray-800 border-gray-700"
              : "bg-white border-gray-200"
          }`}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
        >
          <div className="p-4">
            <h3
              className={`text-sm font-semibold mb-3 ${
                isDarkMode ? "text-white" : "text-gray-900"
              }`}
            >
              사용 가능한 에이전트
            </h3>
            <div className="space-y-3 max-h-[500px] overflow-y-auto">
              {AGENTS.map((agent, index) => (
                <div
                  key={index}
                  className={`flex items-start gap-3 p-2 rounded-md ${
                    isDarkMode ? "hover:bg-gray-700" : "hover:bg-gray-50"
                  } transition-colors`}
                >
                  <span className="text-2xl flex-shrink-0">{agent.icon}</span>
                  <div className="flex-1 min-w-0">
                    <p
                      className={`text-sm font-medium ${
                        isDarkMode ? "text-white" : "text-gray-900"
                      }`}
                    >
                      {agent.name}
                    </p>
                    <p
                      className={`text-xs mt-1 ${
                        isDarkMode ? "text-gray-400" : "text-gray-500"
                      }`}
                    >
                      {agent.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

