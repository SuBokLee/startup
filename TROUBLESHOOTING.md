# 배포 문제 해결 가이드

## 🔴 "서버에 연결할 수 없습니다" 에러 해결

### 문제 원인
프론트엔드(Vercel)가 백엔드(Railway) API에 연결하지 못하고 있습니다.

### 해결 방법

#### 1. Vercel 환경 변수 확인

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard
   - 프로젝트 `startup-apaj` 클릭

2. **Settings → Environment Variables 확인**
   - `NEXT_PUBLIC_API_URL` 변수가 있는지 확인
   - 값이 Railway 백엔드 URL인지 확인
   - 예: `https://your-backend.railway.app`

3. **환경 변수가 없거나 잘못된 경우**
   - Railway에서 백엔드 URL 복사
   - Vercel에 `NEXT_PUBLIC_API_URL` 추가/수정
   - Production, Preview, Development 모두 체크
   - Save 후 Redeploy

#### 2. Railway 백엔드 확인

1. **Railway 대시보드 접속**
   - https://railway.app/dashboard
   - 백엔드 프로젝트 클릭

2. **배포 상태 확인**
   - Deployments 탭에서 배포가 완료되었는지 확인
   - Logs에서 서버가 정상 실행 중인지 확인
   - `Uvicorn running on http://0.0.0.0:8080` 메시지 확인

3. **URL 확인**
   - 프로젝트 페이지 상단에서 URL 복사
   - 또는 Settings → Networking에서 확인

4. **환경 변수 확인**
   - Settings → Variables
   - `ALLOWED_ORIGINS`에 Vercel URL이 포함되어 있는지 확인
   - 예: `https://startup-apaj.vercel.app`

#### 3. CORS 설정 확인

Railway 백엔드의 `ALLOWED_ORIGINS`에 다음이 포함되어야 합니다:
```
https://startup-apaj.vercel.app
```

여러 URL은 쉼표로 구분:
```
https://startup-apaj.vercel.app,http://localhost:3000
```

#### 4. API 엔드포인트 테스트

Railway 백엔드 URL이 정상 작동하는지 확인:

1. **브라우저에서 테스트**
   - `https://your-backend.railway.app/` 접속
   - JSON 응답이 나오는지 확인
   - 예: `{"message":"창업 견인차 API","version":"2.0.0",...}`

2. **curl로 테스트**
   ```bash
   curl https://your-backend.railway.app/
   ```

3. **프론트엔드에서 직접 테스트**
   - 브라우저 개발자 도구 → Console
   - `fetch('https://your-backend.railway.app/').then(r => r.json()).then(console.log)`
   - CORS 에러가 나오면 `ALLOWED_ORIGINS` 확인

## ✅ 체크리스트

- [ ] Railway 백엔드가 배포 완료되었는가?
- [ ] Railway 백엔드 URL을 확인했는가?
- [ ] Vercel에 `NEXT_PUBLIC_API_URL` 환경 변수가 설정되었는가?
- [ ] `NEXT_PUBLIC_API_URL` 값이 Railway 백엔드 URL과 일치하는가?
- [ ] Vercel을 재배포했는가?
- [ ] Railway의 `ALLOWED_ORIGINS`에 Vercel URL이 포함되어 있는가?
- [ ] Railway 백엔드가 정상 실행 중인가? (Logs 확인)

## 🔧 빠른 해결 방법

### Step 1: Railway URL 확인
1. Railway → 프로젝트 → URL 복사
2. 예: `https://your-app.railway.app`

### Step 2: Vercel 환경 변수 설정
1. Vercel → 프로젝트 → Settings → Environment Variables
2. `NEXT_PUBLIC_API_URL` 추가/수정
3. 값: Railway URL
4. 모든 환경 체크 → Save

### Step 3: Railway CORS 설정
1. Railway → 프로젝트 → Settings → Variables
2. `ALLOWED_ORIGINS` 추가/수정
3. 값: `https://startup-apaj.vercel.app`
4. Save (자동 재배포)

### Step 4: 재배포
1. Vercel: Deployments → 최신 배포 → Redeploy
2. Railway: 자동 재배포됨

## 🆘 여전히 안 될 때

1. **브라우저 개발자 도구 확인**
   - F12 → Console 탭
   - Network 탭에서 API 요청 확인
   - 에러 메시지 확인

2. **Railway Logs 확인**
   - Railway → 프로젝트 → Deployments → 최신 배포 → Logs
   - 에러 메시지 확인

3. **Vercel Logs 확인**
   - Vercel → 프로젝트 → Deployments → 최신 배포 → Logs
   - 빌드 에러 확인

