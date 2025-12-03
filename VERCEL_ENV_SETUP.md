# Vercel 환경 변수 설정 가이드

## 📋 필요한 환경 변수 목록

### 필수 환경 변수

1. **`NEXT_PUBLIC_API_URL`**
   - 백엔드 API URL
   - 예: `https://your-backend.railway.app`
   - ⚠️ 아직 Railway 배포 전이라면 일단 `http://localhost:8000`으로 설정하고, 나중에 업데이트

2. **`NEXT_PUBLIC_SUPABASE_URL`**
   - Supabase 프로젝트 URL
   - 예: `https://eymlnoqzmxxkrgahqwqg.supabase.co`

3. **`NEXT_PUBLIC_SUPABASE_ANON_KEY`**
   - Supabase Anon Key (Public Key)
   - 예: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## 🚀 Vercel에서 환경 변수 설정하는 방법

### 방법 1: Vercel 대시보드에서 설정 (추천)

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard
   - 배포 중인 프로젝트 클릭

2. **Settings 탭 클릭**
   - 프로젝트 페이지 상단 메뉴에서 "Settings" 선택

3. **Environment Variables 메뉴 클릭**
   - 왼쪽 사이드바에서 "Environment Variables" 선택

4. **환경 변수 추가**
   - "Add New" 버튼 클릭
   - 각 변수를 하나씩 추가:

   **변수 1:**
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-backend.railway.app` (또는 임시로 `http://localhost:8000`)
   - Environment: `Production`, `Preview`, `Development` 모두 체크
   - "Save" 클릭

   **변수 2:**
   - Key: `NEXT_PUBLIC_SUPABASE_URL`
   - Value: `https://eymlnoqzmxxkrgahqwqg.supabase.co`
   - Environment: 모두 체크
   - "Save" 클릭

   **변수 3:**
   - Key: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5bWxub3F6bXh4a3JnYWhxd3FnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzOTUyMTYsImV4cCI6MjA3OTk3MTIxNn0.BYXyAikSTExnE5aM0LUFILC9eaV4VEO1DaGQi94Jkws`
   - Environment: 모두 체크
   - "Save" 클릭

5. **재배포**
   - 환경 변수 추가 후 자동으로 재배포되거나
   - "Deployments" 탭 → 최신 배포 → "Redeploy" 클릭

### 방법 2: 배포 중 설정

배포 프로세스 중에도 환경 변수를 설정할 수 있습니다:

1. **"Add New Project" 화면에서**
   - "Environment Variables" 섹션 찾기
   - "Add Variable" 클릭
   - 변수 추가

2. **또는 배포 후**
   - Settings → Environment Variables에서 추가

## 📝 실제 값 예시

현재 프로젝트에서 사용 중인 Supabase 정보:
- **URL**: `https://eymlnoqzmxxkrgahqwqg.supabase.co`
- **Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5bWxub3F6bXh4a3JnYWhxd3FnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzOTUyMTYsImV4cCI6MjA3OTk3MTIxNn0.BYXyAikSTExnE5aM0LUFILC9eaV4VEO1DaGQi94Jkws`

**백엔드 URL**은 Railway 배포 후 받은 URL로 업데이트해야 합니다.

## ⚠️ 중요 사항

1. **`NEXT_PUBLIC_` 접두사**
   - Next.js에서 클라이언트 사이드에서 사용할 변수는 반드시 `NEXT_PUBLIC_`로 시작해야 합니다.

2. **환경별 설정**
   - Production: 실제 사용자에게 보이는 환경
   - Preview: Pull Request마다 생성되는 환경
   - Development: 로컬 개발 환경

3. **재배포 필요**
   - 환경 변수를 추가/수정한 후에는 반드시 재배포해야 적용됩니다.

4. **보안**
   - 환경 변수는 암호화되어 저장됩니다.
   - `NEXT_PUBLIC_`로 시작하는 변수는 클라이언트 번들에 포함되므로 민감한 정보는 넣지 마세요.

## 🔄 백엔드 URL 업데이트 방법

Railway 배포 후:

1. Railway에서 백엔드 URL 복사 (예: `https://your-app.railway.app`)
2. Vercel → Settings → Environment Variables
3. `NEXT_PUBLIC_API_URL` 편집
4. 새 URL로 업데이트
5. Redeploy

## ✅ 확인 방법

배포 후 브라우저 콘솔에서 확인:
```javascript
console.log(process.env.NEXT_PUBLIC_API_URL)
console.log(process.env.NEXT_PUBLIC_SUPABASE_URL)
```

또는 Vercel의 Function Logs에서 확인 가능합니다.

