# Railway Public Networking 도메인 설정 가이드

## ✅ Railway Public Networking 도메인 사용

Railway의 **Public Networking**에서 받은 도메인 주소가 **정확히 백엔드 API URL**입니다!

### 도메인 형식
- `https://your-app.railway.app`
- 또는 `https://your-app.up.railway.app`

## 🔧 Vercel 환경 변수에 설정하기

### Step 1: Railway 도메인 복사

1. **Railway 대시보드**
   - 프로젝트 → Settings → Networking
   - 또는 프로젝트 페이지 상단의 Public Domain

2. **도메인 복사**
   - 예: `https://your-app.railway.app`

### Step 2: Vercel 환경 변수 설정

1. **Vercel 대시보드**
   - 프로젝트 → Settings → Environment Variables

2. **`NEXT_PUBLIC_API_URL` 추가/수정**
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: **Railway에서 복사한 도메인** (예: `https://your-app.railway.app`)
   - **Environment**: 다음 3개 모두 체크 ⭐
     - ☑ Production
     - ☑ Preview (필수!)
     - ☑ Development
   - Save 클릭

3. **재배포**
   - Deployments 탭 → 최신 배포 → Redeploy

### Step 3: Railway CORS 설정

1. **Railway → 프로젝트 → Settings → Variables**

2. **`ALLOWED_ORIGINS` 확인/추가**
   - Key: `ALLOWED_ORIGINS`
   - Value: 다음 URL들을 쉼표로 구분:
   ```
   https://startup-apaj.vercel.app,https://startup-apaj-git-main-suboks-projects.vercel.app,http://localhost:3000
   ```
   - Save 클릭

## ✅ 확인 방법

1. **Railway 도메인 테스트**
   - 브라우저에서 Railway 도메인 접속
   - 예: `https://your-app.railway.app/`
   - JSON 응답이 나와야 함: `{"message":"창업 견인차 API",...}`

2. **Vercel 재배포 후**
   - 프리뷰 사이트 접속
   - F12 → Console 탭
   - `🔍 API_URL: [Railway 도메인]` 확인
   - 메시지 전송 테스트

## 💡 중요 사항

- Railway Public Networking 도메인 = 백엔드 API URL ✅
- Vercel 환경 변수에 이 도메인을 설정해야 함
- Preview 환경도 반드시 체크해야 함
- 환경 변수 설정 후 재배포 필수

