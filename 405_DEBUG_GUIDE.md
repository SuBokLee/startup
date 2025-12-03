# 405 오류 디버깅 가이드

## 🔍 405 오류 원인 분석

405 "Method Not Allowed" 오류는 다음과 같은 경우에 발생합니다:

1. **잘못된 URL로 요청** (가장 가능성 높음)
   - 환경 변수가 설정되지 않아서 `http://localhost:8000`으로 요청
   - 프리뷰 환경에 환경 변수가 없음

2. **Railway 백엔드가 작동하지 않음**
   - 배포 실패
   - 서버 다운

3. **CORS 문제**
   - Railway의 `ALLOWED_ORIGINS`에 프리뷰 URL이 없음

## 🔧 해결 방법

### Step 1: 브라우저 개발자 도구로 확인

1. **프리뷰 사이트 접속**
   - https://startup-apaj-git-main-suboks-projects.vercel.app/

2. **F12 → Console 탭**
   - 다음 로그 확인:
     ```
     API_URL: [실제 URL]
     Request URL: [실제 요청 URL]
     ```
   - 만약 `API_URL: http://localhost:8000`이면 → 환경 변수 미설정

3. **Network 탭**
   - `/chat` 요청 클릭
   - Request URL 확인
   - Response 확인

### Step 2: Vercel 환경 변수 확인

1. **Vercel 대시보드**
   - 프로젝트 → Settings → Environment Variables

2. **`NEXT_PUBLIC_API_URL` 확인**
   - 값이 Railway 백엔드 URL인지 확인
   - 예: `https://your-app.railway.app`

3. **Environment 설정 확인**
   - ☑ Production
   - ☑ Preview ⭐ (필수!)
   - ☑ Development

4. **Preview가 체크되지 않은 경우**
   - 편집 → Preview 체크 → Save
   - 프리뷰 배포 재배포

### Step 3: Railway 백엔드 확인

1. **Railway 대시보드**
   - 프로젝트 → Deployments
   - 배포 상태가 "Running"인지 확인

2. **백엔드 URL 테스트**
   - 브라우저에서 `https://your-app.railway.app/` 접속
   - JSON 응답이 나오는지 확인
   - 예: `{"message":"창업 견인차 API",...}`

3. **`/chat` 엔드포인트 테스트**
   - 브라우저 개발자 도구 → Console
   - 다음 명령 실행:
   ```javascript
   fetch('https://your-app.railway.app/chat', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({message: 'test'})
   }).then(r => r.json()).then(console.log).catch(console.error)
   ```

### Step 4: Railway CORS 설정

1. **Railway → 프로젝트 → Settings → Variables**

2. **`ALLOWED_ORIGINS` 확인/추가**
   - 값에 다음 URL들이 포함되어야 함:
   ```
   https://startup-apaj.vercel.app,https://startup-apaj-git-main-suboks-projects.vercel.app,http://localhost:3000
   ```

3. **Save** (자동 재배포)

## 📋 체크리스트

- [ ] 브라우저 Console에서 `API_URL` 로그 확인
- [ ] `API_URL`이 `http://localhost:8000`이 아닌 Railway URL인가?
- [ ] Vercel 환경 변수에 `NEXT_PUBLIC_API_URL`이 설정되어 있는가?
- [ ] Preview 환경이 체크되어 있는가? ⭐
- [ ] Railway 백엔드가 실행 중인가?
- [ ] Railway 백엔드 URL이 올바른가?
- [ ] Railway의 `ALLOWED_ORIGINS`에 프리뷰 URL이 포함되어 있는가?

## 🆘 여전히 안 될 때

브라우저 Console과 Network 탭의 정보를 알려주세요:
1. `API_URL` 로그 값
2. Network 탭의 `/chat` 요청:
   - Request URL
   - Status Code
   - Response

이 정보를 알려주시면 정확한 해결 방법을 제시하겠습니다.

