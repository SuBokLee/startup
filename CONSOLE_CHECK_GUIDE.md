# 브라우저 Console에서 API_URL 확인하는 방법

## 🔍 Console 로그 확인 단계

### Step 1: 프리뷰 사이트 접속

1. **프리뷰 사이트 열기**
   - https://startup-apaj-git-main-suboks-projects.vercel.app/
   - 또는 프로덕션: https://startup-apaj.vercel.app/

### Step 2: 개발자 도구 열기

1. **F12 키 누르기**
   - 또는 마우스 우클릭 → "검사" 또는 "Inspect"

2. **Console 탭 클릭**
   - 개발자 도구 상단의 "Console" 탭 선택

### Step 3: 로그 확인

1. **페이지 새로고침**
   - F5 또는 Ctrl+R (Mac: Cmd+R)

2. **Console에서 다음 로그 찾기**
   ```
   🔍 API_URL: [값]
   🔍 Request URL: [값]
   ```

3. **확인할 내용**
   - `🔍 API_URL:` 뒤에 나오는 값
   - 만약 `http://localhost:8000`이면 → 환경 변수 미설정
   - 만약 Railway 도메인 (예: `https://xxx.railway.app`)이면 → 정상

### Step 4: 메시지 전송 시 로그 확인

1. **채팅 입력창에 메시지 입력**
   - 예: "안녕하세요"

2. **전송 버튼 클릭**

3. **Console에서 로그 확인**
   - `🔍 API_URL:` 로그 확인
   - `🔍 Request URL:` 로그 확인
   - 에러가 있으면 `❌ API Error:` 로그 확인

## 📋 예상되는 로그

### ✅ 정상적인 경우
```
🔍 API_URL: https://your-app.railway.app
🔍 Request URL: https://your-app.railway.app/chat
```

### ❌ 환경 변수가 설정되지 않은 경우
```
❌ NEXT_PUBLIC_API_URL 환경 변수가 설정되지 않았습니다!
❌ 현재 API_URL: http://localhost:8000
❌ 해결 방법:
   1. Vercel → Settings → Environment Variables
   2. NEXT_PUBLIC_API_URL 추가
   3. 값: Railway 백엔드 URL
   4. Preview 환경 체크 필수!
   5. 재배포
🔍 API_URL: http://localhost:8000
🔍 Request URL: http://localhost:8000/chat
```

## 🆘 문제 해결

### API_URL이 `http://localhost:8000`인 경우

1. **Vercel 환경 변수 확인**
   - Vercel → Settings → Environment Variables
   - `NEXT_PUBLIC_API_URL` 변수가 있는지 확인
   - 값이 Railway 도메인인지 확인
   - Preview 환경이 체크되어 있는지 확인

2. **재배포**
   - Deployments → Redeploy

### API_URL이 Railway 도메인인데도 405 오류가 나는 경우

1. **Railway 백엔드 확인**
   - Railway 대시보드 → 프로젝트
   - 배포 상태가 "Running"인지 확인
   - Logs에서 에러 확인

2. **CORS 설정 확인**
   - Railway → Settings → Variables
   - `ALLOWED_ORIGINS`에 Vercel URL이 포함되어 있는지 확인

## 💡 팁

- Console 로그는 페이지를 새로고침하면 다시 나타납니다
- 메시지를 전송할 때마다 로그가 출력됩니다
- Network 탭에서도 실제 요청 URL을 확인할 수 있습니다

