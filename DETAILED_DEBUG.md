# 405 오류 상세 디버깅

## 🔍 단계별 확인

### 1. 브라우저 Console 확인 (가장 중요!)

1. **프리뷰 사이트 접속**
   - https://startup-apaj-git-main-suboks-projects.vercel.app/

2. **F12 → Console 탭**
   - 다음 정보를 확인해주세요:
     - `🔍 API_URL: [어떤 값?]`
     - `🔍 Request URL: [어떤 값?]`
     - `❌ API Error:` 메시지

3. **Network 탭**
   - `/chat` 요청 클릭
   - Request URL 확인
   - Status Code 확인

### 2. Railway 백엔드 직접 테스트

브라우저 Console에서 다음 명령 실행:

```javascript
// Railway 백엔드 URL을 여기에 입력
const backendUrl = 'https://your-railway-url.railway.app';

// 테스트 1: 루트 엔드포인트
fetch(`${backendUrl}/`).then(r => r.json()).then(console.log).catch(console.error);

// 테스트 2: /chat 엔드포인트
fetch(`${backendUrl}/chat`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'test'})
}).then(r => r.json()).then(console.log).catch(console.error);
```

### 3. Vercel 환경 변수 확인

Vercel 대시보드에서:
1. Settings → Environment Variables
2. `NEXT_PUBLIC_API_URL` 값 확인
3. Preview 체크 여부 확인

### 4. Railway 백엔드 상태 확인

Railway 대시보드에서:
1. 프로젝트 → Deployments
2. 최신 배포 상태 확인
3. Logs에서 에러 확인

## 🆘 다음 정보를 알려주세요

1. **브라우저 Console의 `🔍 API_URL` 값**
2. **Railway 백엔드 URL**
3. **Vercel 환경 변수에 설정된 `NEXT_PUBLIC_API_URL` 값**
4. **Railway 배포 상태** (Running인지?)

이 정보를 알려주시면 정확한 해결 방법을 제시하겠습니다.

