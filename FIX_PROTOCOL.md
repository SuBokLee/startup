# 프로토콜 누락 문제 해결

## 🔴 문제 발견

로그를 보면:
```
🔍 API_URL: startup-production-f43b.up.railway.app
```

**프로토콜(`https://`)이 없습니다!**

이로 인해:
- 상대 경로로 인식됨
- `https://startup-apaj.vercel.app/startup-production-f43b.up.railway.app/chat`로 잘못된 요청
- 405 오류 발생

## ✅ 해결 방법

### Step 1: Vercel 환경 변수 수정

1. **Vercel 대시보드**
   - https://vercel.com/dashboard
   - 프로젝트 `startup-apaj` 클릭

2. **Settings → Environment Variables**

3. **`NEXT_PUBLIC_API_URL` 편집**
   - 기존 값: `startup-production-f43b.up.railway.app` (잘못됨)
   - **수정할 값**: `https://startup-production-f43b.up.railway.app` ⭐
   - **중요**: `https://`를 반드시 포함해야 합니다!

4. **Environment 확인**
   - ☑ Production
   - ☑ Preview (필수!)
   - ☑ Development

5. **Save 클릭**

6. **재배포**
   - Deployments 탭 → 최신 배포 → Redeploy 클릭

### Step 2: 확인

재배포 후:
1. 프리뷰 사이트 접속
2. F12 → Console 탭
3. 다음 로그 확인:
   ```
   🔍 API_URL: https://startup-production-f43b.up.railway.app
   🔍 Request URL: https://startup-production-f43b.up.railway.app/chat
   ```
4. 메시지 전송 테스트

## 💡 중요 사항

- 환경 변수 값에 **반드시 `https://`를 포함**해야 합니다
- `https://startup-production-f43b.up.railway.app` ✅
- `startup-production-f43b.up.railway.app` ❌ (프로토콜 없음)

