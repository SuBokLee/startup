# Tavily 웹서칭 설정 가이드

## 1. Tavily API 키 발급

1. [Tavily 웹사이트](https://tavily.com)에 접속
2. 회원가입 또는 로그인
3. 대시보드에서 API 키 발급
4. API 키 복사

## 2. 환경 변수 설정

`backend/.env` 파일을 생성하거나 수정하여 다음을 추가:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

**참고**: `.env` 파일은 `backend` 디렉토리에 있어야 합니다.

## 3. 현재 설정 상태

Tavily는 이미 코드에 통합되어 있습니다:
- ✅ `backend/tools.py`: TavilySearchResults 도구 설정
- ✅ `backend/agents/grant_hunter.py`: 정부 보조금 검색에 사용
- ✅ `backend/agents/market_sensor.py`: 시장 분석에 사용
- ✅ `backend/requirements.txt`: tavily-python 패키지 포함

## 4. 사용 방법

### Grant Hunter 에이전트
- "정부 보조금 찾아줘"
- "K-Startup 프로그램 알려줘"
- "우리 산업에 맞는 지원사업 찾아줘"

### Market Sensor 에이전트
- "경쟁사 분석해줘"
- "시장 트렌드 알려줘"
- "우리 제품의 경쟁력 분석해줘"

## 5. 테스트

API 키를 설정한 후 백엔드 서버를 재시작하면 자동으로 Tavily가 활성화됩니다.

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

## 문제 해결

- **"TAVILY_API_KEY not found"** 경고가 나타나면:
  - `.env` 파일이 `backend` 디렉토리에 있는지 확인
  - API 키가 올바르게 입력되었는지 확인
  - 백엔드 서버를 재시작

- **웹서칭이 작동하지 않으면**:
  - 브라우저 콘솔과 백엔드 로그 확인
  - API 키가 유효한지 확인
  - Tavily 대시보드에서 API 사용량 확인

