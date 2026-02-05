# Kakao Authentication API

FastAPI 기반의 Kakao OAuth 인증 API입니다.

## 기능

- PM-EDDI-1: 환경 변수 로딩을 위한 config/env 초기화
- PM-EDDI-2: Kakao 인증 URL 생성
- PM-EDDI-3: 인가 코드를 받아 Kakao 액세스 토큰 요청
- PM-EDDI-4: 액세스 토큰으로 Kakao 사용자 정보 조회

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
KAKAO_CLIENT_ID=your_kakao_client_id_here
KAKAO_REDIRECT_URI=http://localhost:8000/kakao-authentication/callback
KAKAO_CLIENT_SECRET=your_kakao_client_secret_here
```

### 3. 애플리케이션 실행

```bash
uvicorn main:app --reload
```

## API 엔드포인트

### 1. OAuth 인증 URL 생성

```
GET /kakao-authentication/request-oauth-link
```

**응답:**
```json
{
  "auth_url": "https://kauth.kakao.com/oauth/authorize?client_id=...&redirect_uri=...&response_type=code"
}
```

### 2. 액세스 토큰 요청 및 사용자 정보 조회

```
GET /kakao-authentication/request-access-token-after-redirection?code={인가코드}
```

**응답:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "...",
  "expires_in": 21599,
  "refresh_token_expires_in": 5183999,
  "scope": "...",
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

- **Controller**: 요청/응답 처리만 담당
- **Service Interface**: 비즈니스 로직 인터페이스 정의
- **Service Implementation**: 비즈니스 로직 구현
- **Config**: 환경 변수 기반 설정 관리
- **Models**: 데이터 모델 정의

Controller는 Service Interface에만 의존하며, 구현체에 직접 의존하지 않습니다.

