# GitHub Education을 이용한 쉬운 배포 가이드 🎓

GitHub Education Student Developer Pack을 활용하면 **무료로** 프로덕션 배포가 가능합니다!

## 🎁 GitHub Education 혜택

### 1. Vercel Pro 플랜 (무료) ⭐
- ✅ 무제한 배포
- ✅ 커스텀 도메인
- ✅ 프리뷰 배포
- ✅ **Next.js 최적화** (우리 프로젝트에 완벽!)
- ✅ 자동 HTTPS

### 2. Railway 크레딧
- ✅ $5 무료 크레딧/월
- ✅ 자동 배포
- ✅ GitHub 연동

### 3. 기타 혜택
- DigitalOcean $200 크레딧
- Azure $100 크레딧
- AWS Educate 크레딧

## 🚀 가장 쉬운 방법 (5분 배포)

### Step 1: GitHub Education 인증 (1분)

1. **GitHub Education 가입**
   - https://education.github.com/pack 접속
   - "Get your pack" 클릭
   - 학생 인증 (학교 이메일 또는 학생증)

2. **Vercel Education 플랜 활성화**
   - https://vercel.com/github → "Sign up with GitHub"
   - Education 플랜 선택 (무료 Pro 플랜!)

### Step 2: GitHub에 코드 푸시 (2분)

```bash
# 저장소 초기화 (아직 안 했다면)
git init
git add .
git commit -m "Ready for deployment"

# GitHub에 저장소 생성 후
git remote add origin https://github.com/your-username/startup-assistant.git
git branch -M main
git push -u origin main
```

### Step 3: Vercel 배포 (1분) ⭐ 가장 쉬움!

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard

2. **"Add New Project" 클릭**
   - GitHub 저장소 선택
   - Root Directory: `frontend` 선택
   - Framework Preset: Next.js (자동 감지)

3. **Environment Variables 추가**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```
   (백엔드 URL은 Step 4에서 받은 후 업데이트)

4. **Deploy 클릭!**
   - 자동으로 배포 시작
   - 1-2분 후 URL 생성 (예: `https://startup-assistant.vercel.app`)

### Step 4: Railway 배포 (1분)

1. **Railway 대시보드 접속**
   - https://railway.app → GitHub로 로그인

2. **"New Project" → "Deploy from GitHub repo"**
   - 저장소 선택
   - `backend` 폴더 선택

3. **환경 변수 설정**
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
   (프론트엔드 URL은 Step 3에서 받은 URL 사용)

4. **자동 배포 완료!**
   - Railway가 자동으로 배포
   - URL 생성 (예: `https://your-app.railway.app`)

### Step 5: CORS 업데이트 (30초)

1. **Vercel 환경 변수 업데이트**
   - Vercel 대시보드 → 프로젝트 → Settings → Environment Variables
   - `NEXT_PUBLIC_API_URL`을 Railway에서 받은 백엔드 URL로 업데이트
   - Redeploy 클릭

2. **Railway 환경 변수 업데이트**
   - Railway 대시보드 → 프로젝트 → Variables
   - `ALLOWED_ORIGINS`에 Vercel 프론트엔드 URL 추가
   - 자동 재배포

**끝!** 🎉 이제 누구나 접속할 수 있습니다!

## 🔄 자동 배포 설정 (선택사항)

GitHub에 푸시할 때마다 자동으로 배포되도록 설정하려면:

### GitHub Actions 사용 (이미 설정됨!)

`.github/workflows/` 폴더에 자동 배포 파일이 있습니다.

**필요한 설정:**

1. **Vercel Secrets 추가** (GitHub 저장소 → Settings → Secrets)
   - `VERCEL_TOKEN`: Vercel → Settings → Tokens → Create Token
   - `VERCEL_ORG_ID`: Vercel → Settings → General → Team ID
   - `VERCEL_PROJECT_ID`: Vercel 프로젝트 → Settings → General → Project ID

2. **Railway Secrets 추가**
   - `RAILWAY_TOKEN`: Railway → Account → Tokens → New Token

이제 `git push`만 하면 자동 배포됩니다! 🚀

## 📋 체크리스트

### GitHub Education 인증
- [ ] GitHub Education Pack 가입 완료
- [ ] Vercel Education 플랜 활성화
- [ ] Railway 크레딧 확인

### 저장소 설정
- [ ] 코드를 GitHub에 푸시
- [ ] GitHub Secrets 설정 (자동 배포 사용 시)

### 배포 설정
- [ ] Vercel에 프론트엔드 프로젝트 생성
- [ ] Railway에 백엔드 프로젝트 생성
- [ ] 환경 변수 설정 완료
- [ ] CORS 설정 완료

### 테스트
- [ ] 프론트엔드가 백엔드 API에 연결되는지 확인
- [ ] 모든 기능이 정상 작동하는지 확인

## 💡 왜 이 방법이 가장 쉬운가?

1. **무료**: GitHub Education으로 모든 서비스 무료 이용
2. **자동**: GitHub에 푸시하면 자동 배포
3. **간단**: 클릭 몇 번으로 완료
4. **안정적**: Vercel과 Railway는 업계 표준
5. **빠름**: 5분 안에 배포 완료

## 🆘 문제 해결

### 배포가 안 될 때
1. **Vercel**: Deployments 탭에서 로그 확인
2. **Railway**: Deployments 탭에서 로그 확인
3. **환경 변수**: 모든 필수 변수가 설정되었는지 확인

### API 연결 오류
- `NEXT_PUBLIC_API_URL`이 올바른 백엔드 URL인지 확인
- Railway에서 백엔드가 실행 중인지 확인
- CORS 오류: `ALLOWED_ORIGINS`에 프론트엔드 URL이 포함되어 있는지 확인

### GitHub Education 인증 안 될 때
- 학교 이메일로 재시도
- 학생증 사진 업로드
- GitHub Support에 문의

## 📚 추가 리소스

- GitHub Education: https://education.github.com/pack
- Vercel 문서: https://vercel.com/docs
- Railway 문서: https://docs.railway.app
- GitHub Actions: https://docs.github.com/en/actions

## 🎯 요약

1. GitHub Education 가입 → Vercel Education 플랜 활성화
2. GitHub에 코드 푸시
3. Vercel에서 프론트엔드 배포 (1분)
4. Railway에서 백엔드 배포 (1분)
5. 환경 변수 연결
6. 완료! 🎉

**총 소요 시간: 5분** ⚡
