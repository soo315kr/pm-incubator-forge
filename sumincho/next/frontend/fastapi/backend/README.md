# Kakao Authentication API

FastAPI 기반 Kakao OAuth 인증 API 서버입니다.

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 환경 변수를 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일에 다음 변수들을 설정해야 합니다:
- `KAKAO_CLIENT_ID`: Kakao 개발자 콘솔에서 발급받은 Client ID
- `KAKAO_REDIRECT_URI`: Kakao OAuth 리다이렉트 URI
- `KAKAO_CLIENT_SECRET`: (선택사항) Kakao Client Secret

### 3. 서버 실행

```bash
uvicorn main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

## API 엔드포인트

### 1. Kakao OAuth 인증 URL 생성

**GET** `/kakao-authentication/request-oauth-link`

Kakao OAuth 인증을 위한 URL을 생성합니다.

**응답 예시:**
```json
{
  "oauth_url": "https://kauth.kakao.com/oauth/authorize?client_id=...&redirect_uri=...&response_type=code"
}
```

### 2. 액세스 토큰 요청 및 사용자 정보 조회

**GET** `/kakao-authentication/request-access-token-after-redirection?code={authorization_code}`

인가 코드를 사용하여 액세스 토큰을 발급받고 사용자 정보를 조회합니다.

**쿼리 파라미터:**
- `code` (필수): Kakao OAuth 리다이렉트에서 받은 인가 코드

**응답 예시:**
```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "refresh_token": "...",
  "expires_in": 21599,
  "refresh_token_expires_in": 5183999,
  "scope": "profile_nickname,account_email",
  "user_info": {
    "id": 123456789,
    "nickname": "사용자닉네임",
    "email": "user@example.com",
    "profile_image": "https://..."
  }
}
```

## 아키텍처

이 프로젝트는 Layered Architecture를 따릅니다:

- **Presentation Layer** (`kakao_authentication/presentation/`): API 엔드포인트 및 요청/응답 처리
- **Domain Layer** (`kakao_authentication/domain/`): 비즈니스 로직 및 서비스 인터페이스
- **Config Layer** (`config/`): 환경 변수 로딩 및 설정 관리

## 구현된 기능

- ✅ PM-EDDI-1: 환경 변수 로딩 설정
- ✅ PM-EDDI-2: Kakao 인증 URL 생성
- ✅ PM-EDDI-3: Kakao 액세스 토큰 요청
- ✅ PM-EDDI-4: Kakao 사용자 정보 조회
