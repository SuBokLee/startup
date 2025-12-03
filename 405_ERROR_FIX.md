# 405 오류 해결 가이드

## 🔴 405 오류: Method Not Allowed

405 오류는 보통 다음과 같은 경우에 발생합니다:
1. **환경 변수가 설정되지 않아서** 잘못된 URL로 요청
2. **프리뷰 환경에 환경 변수가 없음**
3. **CORS 문제**

## 🔧 해결 방법

### Step 1: Vercel 환경 변수 확인 (중요!)

프리뷰 배포(`-git-main-`)도 환경 변수가 필요합니다!

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard
   - 프로젝트 `startup-apaj` 클릭

2. **Settings → Environment Variables**
   - 모든 환경 변수 확인

3. **각 환경 변수의 Environment 설정 확인**
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   
   **중요**: 다음 3개 모두 체크되어 있어야 합니다:
   - ☑ Production
   - ☑ Preview ⭐ (프리뷰 배포에 필수!)
   - ☑ Development

4. **Preview가 체크되지 않은 경우**
   - 환경 변수 편집
   - Preview 체크박스 체크
   - Save
   - 프리뷰 배포 재배포

### Step 2: Railway 백엔드 확인

1. **Railway 백엔드가 실행 중인지 확인**
   - Railway 대시보드 → 프로젝트
   - Deployments 탭에서 배포 상태 확인
   - "Running" 상태인지 확인

2. **Railway 백엔드 URL 확인**
   - 프로젝트 페이지 상단에서 URL 복사
   - 예: `https://your-app.railway.app`

3. **백엔드가 정상 작동하는지 테스트**
   - 브라우저에서 `https://your-app.railway.app/` 접속
   - JSON 응답이 나오는지 확인

### Step 3: CORS 설정 확인

Railway 백엔드의 `ALLOWED_ORIGINS`에 다음이 포함되어야 합니다:
```
https://startup-apaj.vercel.app
https://startup-apaj-git-main-suboks-projects.vercel.app
```

여러 URL은 쉼표로 구분:
```
https://startup-apaj.vercel.app,https://startup-apaj-git-main-suboks-projects.vercel.app,http://localhost:3000
```

### Step 4: 브라우저 개발자 도구로 확인

1. **F12 → Console 탭**
   - 에러 메시지 확인
   - 어떤 URL로 요청을 보내는지 확인

2. **Network 탭**
   - `/chat` 요청 확인
   - 요청 URL 확인
   - 응답 상태 코드 확인

## ✅ 체크리스트

- [ ] Vercel 환경 변수에 `NEXT_PUBLIC_API_URL`이 설정되어 있는가?
- [ ] `NEXT_PUBLIC_API_URL`의 Preview 환경이 체크되어 있는가? ⭐
- [ ] Railway 백엔드가 실행 중인가?
- [ ] Railway 백엔드 URL이 올바른가?
- [ ] Railway의 `ALLOWED_ORIGINS`에 프리뷰 URL이 포함되어 있는가?
- [ ] 프리뷰 배포를 재배포했는가?

## 🎯 빠른 해결 방법

1. **Vercel → Settings → Environment Variables**
2. **모든 환경 변수 확인**
3. **Preview 체크박스가 체크되어 있는지 확인** ⭐
4. **없으면 Preview 체크 후 Save**
5. **프리뷰 배포 재배포**

## 🆘 여전히 안 될 때

브라우저 개발자 도구(F12)에서:
1. **Console 탭**: 에러 메시지 확인
2. **Network 탭**: `/chat` 요청 확인
   - 요청 URL이 무엇인지 확인
   - 응답 상태 코드 확인
   - 응답 본문 확인

이 정보를 알려주시면 더 정확히 도와드릴 수 있습니다.

