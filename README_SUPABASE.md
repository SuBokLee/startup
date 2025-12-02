# Supabase 설정 가이드

## 1. Supabase 프로젝트 생성

1. [Supabase](https://supabase.com)에 가입하고 새 프로젝트를 생성합니다.
2. 프로젝트 설정에서 **URL**과 **Anon Key**를 복사합니다.

## 2. 데이터베이스 스키마 설정

1. Supabase 대시보드에서 **SQL Editor**로 이동합니다.
2. `supabase_schema.sql` 파일의 내용을 복사하여 실행합니다.
3. 이 스크립트는 다음을 생성합니다:
   - `conversations` 테이블: 대화 목록 저장
   - `messages` 테이블: 메시지 저장
   - 인덱스 및 RLS 정책

## 3. 환경 변수 설정

프론트엔드 디렉토리에 `.env.local` 파일을 생성하고 다음을 추가합니다:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**참고**: Supabase 대시보드의 **Settings > API**에서 이 값들을 찾을 수 있습니다.

## 4. 백엔드 의존성 설치 (선택사항)

백엔드에서도 Supabase를 사용하려면:

```bash
cd backend
source venv/bin/activate
pip install supabase
```

그리고 `.env` 파일에 추가:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key  # 서비스 역할 키 (서버 전용)
```

## 5. 기능 확인

설정이 완료되면:
- 새 대화를 시작하면 자동으로 저장됩니다.
- 사이드바의 "대화 기록" 버튼을 클릭하여 이전 대화를 불러올 수 있습니다.
- 대화를 삭제할 수 있습니다.

## 문제 해결

- **"Supabase URL and Anon Key must be set"** 경고가 나타나면:
  - `.env.local` 파일이 `frontend` 디렉토리에 있는지 확인
  - 환경 변수 이름이 정확한지 확인 (`NEXT_PUBLIC_` 접두사 필수)
  - 개발 서버를 재시작

- **RLS 정책 오류**가 발생하면:
  - Supabase 대시보드에서 **Authentication > Policies** 확인
  - 필요시 RLS를 비활성화하거나 적절한 정책 추가

