# Gemini API 쿼터 및 모델 오류 해결 가이드

## 🔍 문제 분석

### 1. 429 오류 (Quota Exceeded)
```
limit: 0, model: gemini-2.0-flash
```

이 오류는 **무료 티어가 비활성화**되었거나 **결제 계정이 연결되지 않았음**을 의미합니다.

### 2. 404 오류 (Model Not Found)
모델 이름이 잘못되었거나 해당 모델에 대한 접근 권한이 없을 수 있습니다.

## ✅ 해결 방법

### 방법 1: Google Cloud Console에서 결제 계정 연결

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/

2. **프로젝트 선택**
   - API 키가 생성된 프로젝트 선택

3. **결제 계정 연결**
   - 좌측 메뉴: **결제 (Billing)**
   - **결제 계정 연결** 클릭
   - 결제 정보 입력 (무료 크레딧 사용 가능)

4. **Generative AI API 활성화 확인**
   - **API 및 서비스** > **라이브러리**
   - "Generative Language API" 검색
   - **사용 설정** 확인

### 방법 2: 무료 티어 활성화

1. **API 할당량 확인**
   - **API 및 서비스** > **할당량**
   - "Generative Language API" 선택
   - 무료 티어 할당량 확인

2. **무료 티어 활성화**
   - 할당량이 0이면 무료 티어가 비활성화된 상태
   - 결제 계정 연결 후 자동 활성화

### 방법 3: 모델 이름 수정

현재 코드에서 `gemini-1.5-pro`와 `gemini-1.5-flash`를 사용하도록 수정했습니다.

**사용 가능한 모델:**
- `gemini-1.5-pro` ✅ (권장)
- `gemini-1.5-flash` ✅ (빠른 응답)
- `gemini-pro` (구버전, 가능하면 피하세요)

**사용 불가능한 모델:**
- `gemini-2.0-flash` ❌ (404 오류)
- `gemini-1.5-pro-002` ❌ (404 오류)
- `models/gemini-1.5-pro` ❌ (접두사 불필요)

## 🚀 다음 단계

1. **Google Cloud Console에서 결제 계정 연결**
2. **코드 변경사항 확인** (이미 수정 완료)
3. **로컬 서버 재시작**
4. **테스트**

## 💡 참고

- 무료 티어는 월 15 RPM (Requests Per Minute) 제한이 있습니다
- 결제 계정을 연결하면 더 높은 할당량을 사용할 수 있습니다
- Google은 무료 크레딧을 제공하므로 실제 비용이 발생하지 않을 수 있습니다

