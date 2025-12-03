# Vercel 환경 변수 입력 위치 찾기

## 🔍 Vercel에서 환경 변수 설정하는 정확한 위치

### Step 1: 프로젝트 페이지 접속

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard
   - 로그인

2. **배포된 프로젝트 클릭**
   - 프로젝트 목록에서 배포 중인 프로젝트 선택
   - 프로젝트 이름을 클릭하여 프로젝트 페이지로 이동

### Step 2: Settings 탭 찾기

프로젝트 페이지 상단에 여러 탭이 있습니다:
- **Overview** (홈)
- **Deployments** (배포 목록)
- **Analytics** (분석)
- **Settings** ⭐ ← **여기를 클릭!**

### Step 3: Environment Variables 메뉴 찾기

Settings 탭을 클릭하면 왼쪽 사이드바에 메뉴가 나타납니다:

**왼쪽 사이드바 메뉴:**
- General
- Domains
- **Environment Variables** ⭐ ← **여기를 클릭!**
- Integrations
- Git
- Security
- Functions
- Edge Network
- Logs
- Billing

### Step 4: 환경 변수 추가

"Environment Variables"를 클릭하면:

1. **환경 변수 목록 화면**이 나타납니다
2. **"Add New"** 또는 **"Add"** 버튼 클릭
3. **입력 필드**가 나타납니다:
   - **Key**: 변수 이름 입력 (예: `NEXT_PUBLIC_API_URL`)
   - **Value**: 변수 값 입력 (예: `https://your-backend.railway.app`)
   - **Environment**: 체크박스 선택
     - ☑ Production
     - ☑ Preview
     - ☑ Development
   - **"Save"** 버튼 클릭

## 📋 필요한 환경 변수 3개

### 1. NEXT_PUBLIC_API_URL
- Key: `NEXT_PUBLIC_API_URL`
- Value: `https://your-backend.railway.app` (Railway에서 받은 URL)
- Environment: 모두 체크

### 2. NEXT_PUBLIC_SUPABASE_URL
- Key: `NEXT_PUBLIC_SUPABASE_URL`
- Value: `https://eymlnoqzmxxkrgahqwqg.supabase.co`
- Environment: 모두 체크

### 3. NEXT_PUBLIC_SUPABASE_ANON_KEY
- Key: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5bWxub3F6bXh4a3JnYWhxd3FnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzOTUyMTYsImV4cCI6MjA3OTk3MTIxNn0.BYXyAikSTExnE5aM0LUFILC9eaV4VEO1DaGQi94Jkws`
- Environment: 모두 체크

## 🆘 Environment Variables 메뉴가 안 보일 때

### 방법 1: 프로젝트 권한 확인
- 프로젝트 소유자 또는 팀 멤버여야 합니다
- 권한이 없으면 소유자에게 요청

### 방법 2: 다른 위치에서 확인
1. **프로젝트 페이지 → Settings**
2. **General 탭**에서 확인
   - 일부 버전에서는 General 탭 하단에 환경 변수 섹션이 있을 수 있습니다

### 방법 3: 배포 중 설정
1. **Deployments 탭** 클릭
2. **최신 배포** 클릭
3. 배포 상세 페이지에서 환경 변수 설정 가능

### 방법 4: 프로젝트 재생성 시 설정
1. **"Add New Project"** 클릭
2. GitHub 저장소 선택
3. **"Configure Project"** 화면에서
4. **"Environment Variables"** 섹션 찾기
5. 여기서 미리 설정 가능

## 📸 화면 구성 (참고)

```
Vercel 대시보드
└── 프로젝트 목록
    └── [프로젝트 이름] 클릭
        └── 프로젝트 페이지
            ├── Overview
            ├── Deployments
            ├── Analytics
            └── Settings ⭐ 클릭
                └── 왼쪽 사이드바
                    ├── General
                    ├── Domains
                    ├── Environment Variables ⭐ 클릭
                    ├── Integrations
                    └── ...
```

## ✅ 환경 변수 추가 후

1. **모든 변수 추가 완료**
2. **자동 재배포** 또는
3. **Deployments 탭 → 최신 배포 → "Redeploy"** 클릭

## 💡 팁

- 환경 변수는 추가/수정 후 **재배포**해야 적용됩니다
- `NEXT_PUBLIC_` 접두사가 있는 변수만 클라이언트에서 사용 가능합니다
- Production, Preview, Development 모두 체크하는 것을 권장합니다

