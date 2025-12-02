# FounderOS - AI Assistant for Startup Founders

FounderOS는 스타트업 창업자를 위한 종합 AI 어시스턴트 시스템입니다. Multi-Agent Architecture를 사용하여 5개의 전문 에이전트를 통합합니다.

## 🎯 핵심 기능 (5개 에이전트)

1. **Virtual Co-founder**: 논리적 토론, 비즈니스 모델 생성, 멘탈 지원
2. **VC Simulator**: 피치덱 리뷰, 까다로운 질문, 투자자 매칭
3. **Grant Hunter**: 정부 보조금 검색, 필터링, 신청서 작성
4. **Market Sensor**: 경쟁사 추적, 감정 분석, 트렌드 발견
5. **MVP Builder**: PRD 생성, 랜딩 페이지 코딩, 간단한 프로토타이핑

## 🏗️ 아키텍처

- **Supervisor Agent**: LangGraph를 사용한 라우팅 시스템
- 사용자는 Supervisor와 대화하며, Supervisor가 적절한 전문 에이전트로 요청을 라우팅합니다.

## 🛠️ 기술 스택

### Backend
- Python FastAPI
- LangChain & LangGraph
- OpenAI API

### Frontend
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Shadcn UI (커스텀 구현)
- Lucide React (아이콘)

## 📁 프로젝트 구조

```
과제5/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── supervisor.py
│   │   ├── cofounder.py
│   │   ├── vc_coach.py
│   │   ├── grant_hunter.py
│   │   ├── market_sensor.py
│   │   └── mvp_builder.py
│   ├── main.py
│   ├── prompts.py
│   └── requirements.txt
└── frontend/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   └── globals.css
    ├── components/
    │   ├── ChatInterface.tsx
    │   └── ui/
    │       ├── button.tsx
    │       ├── input.tsx
    │       ├── card.tsx
    │       └── avatar.tsx
    ├── lib/
    │   └── utils.ts
    └── package.json
```

## 🚀 시작하기

### Backend 설정

1. Backend 디렉토리로 이동:
```bash
cd backend
```

2. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정:
```bash
cp .env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 설정하세요
```

5. 서버 실행:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend 설정

1. Frontend 디렉토리로 이동:
```bash
cd frontend
```

2. 의존성 설치:
```bash
npm install
```

3. 개발 서버 실행:
```bash
npm run dev
```

4. 브라우저에서 `http://localhost:3000` 접속

## 📡 API 엔드포인트

### REST API
- `POST /chat`: 채팅 메시지 전송
  ```json
  {
    "message": "사용자 메시지",
    "conversation_id": "선택적 대화 ID"
  }
  ```

### WebSocket
- `WS /ws`: 실시간 채팅 (향후 구현)

## 🔄 작동 방식

1. 사용자가 메시지를 입력합니다.
2. Supervisor Agent가 메시지를 분석합니다.
3. Supervisor가 적절한 전문 에이전트를 선택합니다.
4. 선택된 에이전트가 작업을 수행하고 응답을 반환합니다.
5. Supervisor가 응답을 사용자에게 전달합니다.

## 📝 다음 단계

- [ ] 각 에이전트의 고급 기능 구현
- [ ] 대화 기록 저장 (데이터베이스 연동)
- [ ] WebSocket 실시간 통신 개선
- [ ] 에이전트별 특화 기능 추가
- [ ] UI/UX 개선

## 📄 라이선스

MIT License

