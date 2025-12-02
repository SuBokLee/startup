import * as React from "react"
import { cn } from "@/lib/utils"

const Avatar = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    variant?: "user" | "supervisor" | "agent"
    agentName?: string
  }
>(({ className, variant = "user", agentName, ...props }, ref) => {
  const getInitials = () => {
    if (agentName) {
      return agentName
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    }
    if (variant === "user") return "U"
    if (variant === "supervisor") return "S"
    return "A"
  }

  const getColor = () => {
    if (variant === "user") return "bg-blue-500"
    if (variant === "supervisor") return "bg-purple-500"
    
    // 에이전트별 색상 매핑
    if (agentName) {
      const agentColors: Record<string, string> = {
        // 영어 이름
        "Cofounder": "bg-indigo-500",
        "VC Simulator": "bg-red-500",
        "Grant Hunter": "bg-yellow-500",
        "Market Sensor": "bg-teal-500",
        "MVP Builder": "bg-orange-500",
        "Framework Designer": "bg-pink-500",
        "Growth Hacker": "bg-cyan-500",
        "Legal Advisor": "bg-emerald-500",
        "Master": "bg-purple-500",
        // 에이전트 키도 지원
        "cofounder": "bg-indigo-500",
        "vc_simulator": "bg-red-500",
        "grant_hunter": "bg-yellow-500",
        "market_sensor": "bg-teal-500",
        "mvp_builder": "bg-orange-500",
        "framework_designer": "bg-pink-500",
        "growth_hacker": "bg-cyan-500",
        "legal_advisor": "bg-emerald-500",
        "supervisor": "bg-purple-500",
      }
      return agentColors[agentName] || "bg-green-500"
    }
    
    return "bg-green-500"
  }

  return (
    <div
      ref={ref}
      className={cn(
        "flex h-10 w-10 items-center justify-center rounded-full text-white font-semibold text-sm",
        getColor(),
        className
      )}
      {...props}
    >
      {getInitials()}
    </div>
  )
})
Avatar.displayName = "Avatar"

export { Avatar }

