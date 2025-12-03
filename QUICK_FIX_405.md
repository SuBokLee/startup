# 405 오류 빠른 해결 가이드

## 🔴 문제: Failed to load resource: the server responded with a status of 405

이 오류는 **프론트엔드가 잘못된 URL로 요청**을 보내고 있을 때 발생합니다.

## ✅ 즉시 해결 방법

### Step 1: Vercel 환경 변수 확인 (가장 중요!)

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard
   - 프로젝트 `startup-apaj` 클릭

2. **Settings → Environment Variables**
   - `NEXT_PUBLIC_API_URL` 변수가 있는지 확인
   - **없으면 추가**, **있으면 값 확인**

3. **환경 변수 추가/수정**
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: **Railway 백엔드 URL** (예: `https://your-app.railway.app`)
   - **Environment**: 다음 3개 모두 체크 ⭐
     - ☑ Production
     - ☑ Preview
     - ☑ Development
   - Save 클릭

4. **재배포**
   - Deployments 탭 → 최신 배포 → Redeploy
   - 또는 새 커밋 푸시로 자동 재배포

### Step 2: Railway 백엔드 URL 확인

1. **Railway 대시보드**
   - https://railway.app/dashboard
   - 백엔드 프로젝트 클릭

2. **URL 복사**
   - 프로젝트 페이지 상단에서 URL 복사
   - 예: `https://your-app.railway.app`

3. **백엔드 테스트**
   - 브라우저에서 `https://your-app.railway.app/` 접속
   - JSON 응답이 나오는지 확인
   - 예: `{"message":"창업 견인차 API",...}`

### Step 3: Railway CORS 설정

1. **Railway → 프로젝트 → Settings → Variables**

2. **`ALLOWED_ORIGINS` 확인/추가**
   - 값에 다음 URL 포함:
   ```
   https://startup-apaj.vercel.app,https://startup-apaj-git-main-suboks-projects.vercel.app,http://localhost:3000
   ```

3. **Save** (자동 재배포)

## 🔍 확인 방법

### 브라우저 개발자 도구

1. **F12 → Console 탭**
   - 다음 로그 확인:
     ```
     🔍 API_URL: [값]
     🔍 Request URL: [값]
     ```
   - 만약 `API_URL: http://localhost:8000`이면 → 환경 변수 미설정

2. **Network 탭**
   - `/chat` 요청 클릭
   - Request URL 확인
   - Status Code 확인 (405)

## 📋 체크리스트

- [ ] Vercel에 `NEXT_PUBLIC_API_URL` 환경 변수가 있는가?
- [ ] 값이 Railway 백엔드 URL인가? (localhost가 아님)
- [ ] Preview 환경이 체크되어 있는가? ⭐
- [ ] Vercel을 재배포했는가?
- [ ] Railway 백엔드가 실행 중인가?
- [ ] Railway의 `ALLOWED_ORIGINS`에 프리뷰 URL이 있는가?

## 🎯 가장 가능성 높은 원인

**Vercel 환경 변수가 설정되지 않았거나 Preview 환경이 체크되지 않음**

→ 프론트엔드가 `http://localhost:8000`으로 요청
→ 405 오류 발생

## 💡 해결 순서

1. Railway 백엔드 URL 확인
2. Vercel 환경 변수에 추가 (Preview 체크 필수!)
3. 재배포
4. 브라우저 Console에서 `🔍 API_URL` 로그 확인

