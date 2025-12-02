# GitHub Actions 자동 배포 설정 가이드

## 필요한 Secrets 설정

### Vercel Secrets
1. Vercel 대시보드 → Settings → Tokens → Create Token
2. GitHub 저장소 → Settings → Secrets and variables → Actions
3. 다음 Secrets 추가:
   - `VERCEL_TOKEN`: Vercel에서 생성한 토큰
   - `VERCEL_ORG_ID`: Vercel Settings → General → Team ID
   - `VERCEL_PROJECT_ID`: Vercel 프로젝트 생성 후 → Settings → General → Project ID

### Railway Secrets
1. Railway 대시보드 → Account → Tokens → New Token
2. GitHub 저장소 → Settings → Secrets and variables → Actions
3. 다음 Secret 추가:
   - `RAILWAY_TOKEN`: Railway에서 생성한 토큰

## 사용법

1. `backend/` 폴더 변경 시 → Railway에 자동 배포
2. `frontend/` 폴더 변경 시 → Vercel에 자동 배포
3. `main` 브랜치에 푸시하면 자동으로 프로덕션 배포

## 수동 배포

GitHub Actions 탭에서 "Run workflow" 버튼으로 수동 실행도 가능합니다.

