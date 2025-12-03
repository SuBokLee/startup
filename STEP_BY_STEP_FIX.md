# 405 오류 단계별 해결 가이드

## 🔴 현재 상황
- 에러: `Server error: 405 -`
- 프론트엔드가 백엔드에 연결하지 못함

## ✅ 필수 확인 사항

### Step 1: Railway 백엔드 URL 확인

1. **Railway 대시보드**
   - https://railway.app/dashboard
   - 백엔드 프로젝트 클릭

2. **URL 복사**
   - 프로젝트 페이지 상단에서 URL 복사
   - 예: `https://your-app.railway.app`
   - 또는 `https://your-app.up.railway.app`

3. **백엔드 테스트**
   - 브라우저에서 Railway URL 접속
   - 예: `https://your-app.railway.app/`
   - JSON 응답이 나와야 함: `{"message":"창업 견인차 API",...}`

### Step 2: Vercel 환경 변수 설정 (가장 중요!)

1. **Vercel 대시보드**
   - https://vercel.com/dashboard
   - 프로젝트 `startup-apaj` 클릭

2. **Settings → Environment Variables**

3. **`NEXT_PUBLIC_API_URL` 확인/추가**
   - 변수가 없으면: "Add New" 클릭
   - 변수가 있으면: 편집 클릭
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: **Step 1에서 복사한 Railway URL** (예: `https://your-app.railway.app`)
   - **Environment**: 다음 3개 모두 체크 ⭐⭐⭐
     - ☑ Production
     - ☑ Preview (프리뷰 배포에 필수!)
     - ☑ Development
   - Save 클릭

4. **재배포**
   - Deployments 탭 → 최신 배포 → "Redeploy" 클릭
   - 또는 새 커밋 푸시로 자동 재배포

### Step 3: Railway CORS 설정

1. **Railway → 프로젝트 → Settings → Variables**

2. **`ALLOWED_ORIGINS` 확인/추가**
   - 변수가 없으면: "New Variable" 클릭
   - Key: `ALLOWED_ORIGINS`
   - Value: 다음 URL들을 쉼표로 구분하여 입력:
   ```
   https://startup-apaj.vercel.app,https://startup-apaj-git-main-suboks-projects.vercel.app,http://localhost:3000
   ```
   - Save 클릭 (자동 재배포)

### Step 4: 확인

1. **Vercel 재배포 완료 후**
   - 프리뷰 사이트 접속: https://startup-apaj-git-main-suboks-projects.vercel.app/

2. **F12 → Console 탭**
   - `🔍 API_URL: [Railway URL]` 확인
   - `⚠️ 환경 변수가 설정되지 않았습니다!` 경고가 없어야 함

3. **메시지 전송 테스트**
   - 채팅 입력 후 전송
   - 405 오류가 사라져야 함

## 🆘 여전히 안 될 때

### 확인할 정보

1. **Railway 백엔드 URL** (예: `https://xxx.railway.app`)
2. **Vercel 환경 변수 값** (`NEXT_PUBLIC_API_URL`의 실제 값)
3. **브라우저 Console의 `🔍 API_URL` 로그 값**
4. **Railway 배포 상태** (Running/Failed)

이 정보를 알려주시면 정확한 해결 방법을 제시하겠습니다.

## 💡 빠른 체크리스트

- [ ] Railway 백엔드 URL 확인 및 복사
- [ ] Vercel에 `NEXT_PUBLIC_API_URL` 환경 변수 추가
- [ ] Preview 환경 체크 (필수!)
- [ ] Vercel 재배포
- [ ] Railway의 `ALLOWED_ORIGINS`에 프리뷰 URL 추가
- [ ] 브라우저 Console에서 `🔍 API_URL` 확인

