import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Startup Sherpa - 창업을 도와주는 짐꾼이자 길잡이',
  description: '스타트업 창업자를 위한 종합 AI 어시스턴트 - 멀티 에이전트 아키텍처',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}

