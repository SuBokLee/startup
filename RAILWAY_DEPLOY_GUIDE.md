# Railway 배포 가이드 - Backend 폴더 선택

## 🚀 Railway에서 Backend 폴더 선택하는 방법

### 방법 1: 프로젝트 생성 시 Root Directory 설정 (추천)

1. **"New Project" → "Deploy from GitHub repo"**
   - GitHub 저장소 선택: `SuBokLee/startup`

2. **"Configure" 또는 "Settings" 클릭**
   - 배포 설정 화면에서 찾기

3. **Root Directory 설정**
   - "Root Directory" 또는 "Working Directory" 필드 찾기
   - 값 입력: `backend`
   - 또는 드롭다운에서 선택

4. **Deploy 클릭**

### 방법 2: 배포 후 Settings에서 변경

1. **프로젝트 대시보드 접속**
   - Railway 대시보드 → 배포된 프로젝트 클릭

2. **Settings 탭 클릭**
   - 프로젝트 페이지 상단 메뉴

3. **Service 탭 선택**
   - 왼쪽 사이드바에서 "Service" 선택

4. **Root Directory 설정**
   - "Root Directory" 필드 찾기
   - 값 입력: `backend`
   - "Save" 클릭
   - 자동으로 재배포됨

### 방법 3: railway.json 파일 사용 (이미 설정됨!)

프로젝트에 `backend/railway.json` 파일이 이미 있습니다.
Railway는 자동으로 이 파일을 인식합니다.

하지만 **Root Directory를 `backend`로 설정**해야 합니다.

## 📋 Railway 배포 설정 체크리스트

### 1. Root Directory 설정
- ✅ Root Directory: `backend`

### 2. Start Command 설정
- Railway가 자동으로 감지하거나
- 수동 설정: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Build Command (선택사항)
- `pip install -r requirements.txt`

### 4. 환경 변수 설정
다음 변수들을 추가해야 합니다:

```
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
SUPABASE_URL=https://eymlnoqzmxxkrgahqwqg.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5bWxub3F6bXh4a3JnYWhxd3FnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzOTUyMTYsImV4cCI6MjA3OTk3MTIxNn0.BYXyAikSTExnE5aM0LUFILC9eaV4VEO1DaGQi94Jkws
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

⚠️ **ALLOWED_ORIGINS**는 Vercel에서 받은 프론트엔드 URL로 업데이트해야 합니다.

## 🔍 Railway UI에서 찾는 방법

### Root Directory 필드 위치

1. **프로젝트 생성 시:**
   - "Deploy from GitHub repo" 화면
   - "Configure" 또는 "Settings" 버튼 클릭
   - "Root Directory" 또는 "Working Directory" 필드

2. **배포 후:**
   - 프로젝트 → Settings → Service
   - "Root Directory" 필드

### 만약 Root Directory 필드가 안 보이면:

1. **Service 탭 확인**
   - Settings → Service → "Root Directory"

2. **Variables 탭에서 확인**
   - Settings → Variables
   - `RAILWAY_ROOT_DIRECTORY` 변수 추가 가능

3. **railway.toml 파일 생성** (고급)
   - 프로젝트 루트에 `railway.toml` 생성
   - 내용:
   ```toml
   [build]
   builder = "NIXPACKS"
   
   [deploy]
   startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
   ```
   - 하지만 Root Directory는 UI에서 설정해야 함

## ✅ 확인 방법

배포 후:

1. **Deployments 탭 확인**
   - 배포 로그에서 `backend/` 폴더의 파일들이 보이는지 확인
   - `requirements.txt`가 인식되는지 확인

2. **Logs 확인**
   - 배포 로그에서 `pip install -r requirements.txt` 실행되는지 확인
   - `uvicorn main:app` 실행되는지 확인

3. **URL 확인**
   - 배포 완료 후 생성된 URL 확인
   - 예: `https://your-app.railway.app`
   - 이 URL을 Vercel의 `NEXT_PUBLIC_API_URL`에 추가

## 🆘 문제 해결

### Root Directory 필드를 못 찾을 때

1. **Railway UI 업데이트 확인**
   - 최신 버전의 Railway 사용 중인지 확인

2. **Service 재생성**
   - 기존 Service 삭제
   - 새로 생성하면서 Root Directory 설정

3. **GitHub Actions 사용**
   - `.github/workflows/deploy-backend.yml` 사용
   - 자동으로 `backend` 폴더 인식

### 배포가 실패할 때

1. **로그 확인**
   - Deployments → 최신 배포 → Logs 클릭
   - 에러 메시지 확인

2. **requirements.txt 확인**
   - `backend/requirements.txt` 파일이 있는지 확인

3. **main.py 확인**
   - `backend/main.py` 파일이 있는지 확인

## 📝 요약

1. Railway 프로젝트 생성
2. GitHub 저장소 연결: `SuBokLee/startup`
3. **Root Directory: `backend` 설정** ⭐
4. 환경 변수 추가
5. Deploy
6. 배포된 URL 복사
7. Vercel의 `NEXT_PUBLIC_API_URL` 업데이트

