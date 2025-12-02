# 창업 견인차 배포 가이드

다른 사람들이 사용할 수 있도록 플랫폼을 배포하는 방법입니다.

> 💡 **GitHub Education 사용자라면?** → `GITHUB_EDUCATION_DEPLOY.md` 파일을 먼저 확인하세요! 더 쉽고 무료로 배포할 수 있습니다.

## 배포 옵션

### 1. 프론트엔드 배포 (Next.js)

#### 옵션 A: Vercel (추천 - Next.js 최적화)
1. **Vercel 계정 생성**: https://vercel.com
2. **프로젝트 연결**:
   ```bash
   cd frontend
   npm install -g vercel
   vercel login
   vercel
   ```
3. **환경 변수 설정** (Vercel 대시보드):
   - `NEXT_PUBLIC_API_URL`: 백엔드 API URL (예: `https://your-backend.railway.app`)
   - Supabase 관련 변수들 (이미 설정되어 있다면 유지)

#### 옵션 B: Netlify
1. **Netlify 계정 생성**: https://netlify.com
2. **GitHub에 코드 푸시**
3. **Netlify에서 GitHub 저장소 연결**
4. **빌드 설정**:
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/.next`

### 2. 백엔드 배포 (FastAPI)

#### 옵션 A: Railway (추천 - 간단함)
1. **Railway 계정 생성**: https://railway.app
2. **새 프로젝트 생성** → "Deploy from GitHub repo"
3. **환경 변수 설정**:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```
4. **시작 명령어 설정**:
   ```
   cd backend && pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

#### 옵션 B: Render
1. **Render 계정 생성**: https://render.com
2. **새 Web Service 생성**
3. **GitHub 저장소 연결**
4. **설정**:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3

#### 옵션 C: Fly.io
1. **Fly.io 계정 생성**: https://fly.io
2. **설치 및 로그인**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```
3. **프로젝트 초기화**:
   ```bash
   cd backend
   fly launch
   ```
4. **환경 변수 설정**: `fly secrets set GOOGLE_API_KEY=...`

### 3. 데이터베이스 (Supabase)
- 이미 클라우드 서비스이므로 추가 배포 불필요
- RLS 정책이 올바르게 설정되어 있는지 확인

## 배포 전 준비사항

### 1. 환경 변수 정리

**프론트엔드** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**백엔드** (`.env`):
```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 2. CORS 설정 확인

백엔드 `main.py`에서 프론트엔드 URL을 업데이트:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-domain.vercel.app",  # 배포된 프론트엔드 URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. 프론트엔드 API URL 수정

`frontend/components/ChatInterface.tsx`에서:
```typescript
// 개발 환경
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// 프로덕션에서는 환경 변수 사용
const response = await fetch(`${API_URL}/chat`, {
  // ...
});
```

## 빠른 배포 (Railway + Vercel)

### Step 1: 백엔드 배포 (Railway)
1. Railway에 로그인
2. "New Project" → "Deploy from GitHub repo"
3. `backend` 폴더 선택
4. 환경 변수 추가
5. 배포 완료 후 URL 복사 (예: `https://your-app.railway.app`)

### Step 2: 프론트엔드 배포 (Vercel)
1. Vercel에 로그인
2. "Add New Project" → GitHub 저장소 선택
3. Root Directory: `frontend`
4. Environment Variables:
   - `NEXT_PUBLIC_API_URL`: Railway에서 받은 백엔드 URL
5. Deploy

### Step 3: CORS 업데이트
Railway에서 받은 백엔드 URL을 `main.py`의 CORS 설정에 추가하고 재배포

## 무료 배포 옵션 요약

| 서비스 | 프론트엔드 | 백엔드 | 무료 티어 |
|--------|-----------|--------|----------|
| Vercel | ✅ | ❌ | ✅ |
| Netlify | ✅ | ❌ | ✅ |
| Railway | ❌ | ✅ | ✅ (제한적) |
| Render | ❌ | ✅ | ✅ (제한적) |
| Fly.io | ❌ | ✅ | ✅ |

## 추천 조합

**가장 간단한 방법**:
- 프론트엔드: **Vercel** (Next.js 최적화, 자동 배포)
- 백엔드: **Railway** (간단한 설정, 자동 배포)

## 주의사항

1. **API 키 보안**: 환경 변수로 관리, 코드에 직접 작성하지 않기
2. **CORS**: 배포된 프론트엔드 URL을 백엔드 CORS에 추가
3. **Supabase RLS**: 프로덕션 환경에 맞게 정책 확인
4. **비용**: 무료 티어는 제한이 있으므로 사용량 모니터링

## 배포 후 확인사항

- [ ] 프론트엔드가 백엔드 API에 연결되는지 확인
- [ ] 인증이 정상 작동하는지 확인
- [ ] 실시간 채팅이 작동하는지 확인
- [ ] 에이전트들이 정상 응답하는지 확인

