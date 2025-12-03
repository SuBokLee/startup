# Railway 배포 URL 확인 방법

## 🚀 Railway에서 URL 확인하는 방법

### 방법 1: 프로젝트 대시보드에서 확인 (가장 쉬움)

1. **Railway 대시보드 접속**
   - https://railway.app/dashboard

2. **배포된 프로젝트 클릭**
   - 프로젝트 목록에서 배포 중인 프로젝트 선택

3. **URL 확인**
   - 프로젝트 페이지 상단에 **도메인 URL**이 표시됩니다
   - 예: `https://your-app.railway.app`
   - 또는 `https://your-app.up.railway.app`

4. **클릭하여 복사**
   - URL을 클릭하면 복사됩니다
   - 또는 URL 옆에 복사 버튼이 있을 수 있습니다

### 방법 2: Settings → Networking에서 확인

1. **프로젝트 → Settings 탭**
   - 프로젝트 페이지 상단 메뉴

2. **Networking 탭 선택**
   - 왼쪽 사이드바에서 "Networking" 선택

3. **Domains 섹션 확인**
   - "Railway Domain" 또는 "Custom Domain" 섹션
   - 여기에 배포된 URL이 표시됩니다

### 방법 3: Deployments 탭에서 확인

1. **프로젝트 → Deployments 탭**
   - 프로젝트 페이지 상단 메뉴

2. **최신 배포 클릭**
   - 가장 최근 배포를 클릭

3. **배포 상세 정보 확인**
   - 배포 로그나 상세 정보에 URL이 표시될 수 있습니다

## 📋 URL 형식

Railway URL은 보통 다음과 같은 형식입니다:

- `https://[프로젝트명].railway.app`
- `https://[프로젝트명].up.railway.app`
- 또는 커스텀 도메인을 설정한 경우 해당 도메인

## ✅ URL 확인 후 해야 할 일

1. **URL 복사**
   - 예: `https://your-backend.railway.app`

2. **Vercel 환경 변수 업데이트**
   - Vercel 대시보드 → 프로젝트 → Settings → Environment Variables
   - `NEXT_PUBLIC_API_URL` 편집
   - Railway URL로 업데이트
   - 예: `https://your-backend.railway.app`

3. **Railway 환경 변수 업데이트**
   - Railway → 프로젝트 → Settings → Variables
   - `ALLOWED_ORIGINS` 편집
   - Vercel 프론트엔드 URL 추가
   - 예: `https://your-frontend.vercel.app`

4. **재배포**
   - Vercel: 자동 재배포 또는 수동 Redeploy
   - Railway: 자동 재배포

## 🔍 URL이 안 보일 때

1. **배포가 아직 진행 중인지 확인**
   - Deployments 탭에서 배포 상태 확인
   - "Building" 또는 "Deploying" 상태면 완료될 때까지 대기

2. **배포가 실패했는지 확인**
   - Deployments 탭 → 최신 배포 → Logs 확인
   - 에러가 있으면 수정 후 재배포

3. **Service가 생성되었는지 확인**
   - 프로젝트에 Service가 있는지 확인
   - Service가 없으면 새로 생성

## 💡 팁

- Railway URL은 배포가 완료되어야 생성됩니다
- 첫 배포는 몇 분 걸릴 수 있습니다
- URL은 프로젝트당 하나씩 생성됩니다
- 커스텀 도메인을 설정할 수도 있습니다 (Settings → Networking)

