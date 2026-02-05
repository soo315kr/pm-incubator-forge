# Kakao OAuth Authentication API

Kakao OAuth 인증 시스템을 구현한 FastAPI 백엔드 프로젝트입니다.

## 구현된 기능

### PM-BH-1: 환경 변수 로딩
- `.env` 파일을 통한 환경 변수 관리
- `config/env.py` 모듈에서 일관된 환경 변수 로딩
- 애플리케이션 시작 시 1회 로드

### PM-BH-2: Kakao 인증 URL 생성
- **엔드포인트**: `GET /kakao-authentication/request-oauth-link`
- Kakao OAuth 인증 페이지 URL 생성 및 반환
- client_id, redirect_uri, response_type 파라미터 포함

### PM-BH-3: 액세스 토큰 발급
- **엔드포인트**: `GET /kakao-authentication/callback?code={code}`
- 인가 코드로 Kakao 액세스 토큰 요청
- 액세스 토큰, 리프레시 토큰, 만료 시간 반환

### PM-BH-4: 사용자 정보 조회
- **엔드포인트**: `GET /kakao-authentication/user-info?access_token={token}`
- 액세스 토큰으로 Kakao 사용자 정보 조회
- 사용자 ID, 닉네임, 이메일 등 반환

## 아키텍처

### Layered Architecture
- **Controller**: HTTP 요청/응답 처리, Service Interface에만 의존
- **Service Interface**: 비즈니스 로직 추상화
- **Service Implementation**: 실제 비즈니스 로직 구현
- **Config**: 환경 변수 및 설정 관리

### 디렉토리 구조
```
backend/
├── config/                      # PM-BH-1: 환경 변수 관리
│   ├── __init__.py
│   └── env.py                   # 환경 변수 로딩
├── kakao_authentication/        # PM-BH-2,3,4: Kakao OAuth 도메인
│   ├── __init__.py
│   ├── service_interface.py     # Service 인터페이스
│   ├── service_implementation.py # Service 구현체
│   └── controller.py            # API 엔드포인트
├── main.py                      # FastAPI 앱 엔트리포인트
├── requirements.txt             # Python 패키지 의존성
├── .env.example                 # 환경 변수 예시
└── README.md
```

## 설치 및 실행

### 1. 가상 환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env.example`을 복사하여 `.env` 파일을 생성하고 값을 입력합니다:
```bash
cp .env.example .env
```

`.env` 파일 내용:
```
KAKAO_CLIENT_ID=your_kakao_client_id_here
KAKAO_REDIRECT_URI=http://localhost:2501/kakao-authentication/callback
```

> Kakao Developers (https://developers.kakao.com/)에서 애플리케이션을 생성하고 REST API 키를 발급받으세요.

### 4. 서버 실행
```bash
# 개발 모드 (자동 리로드)
python main.py

# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. API 문서 확인
브라우저에서 다음 URL을 열어 자동 생성된 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 사용 예시

### 1. Kakao 인증 URL 생성
```bash
curl http://localhost:2501/kakao-authentication/request-oauth-link
```

**응답:**
```json
{
  "oauth_url": "https://kauth.kakao.com/oauth/authorize?client_id=...&redirect_uri=...&response_type=code"
}
```

### 2. 액세스 토큰 발급
```bash
curl "http://localhost:2501/kakao-authentication/callback?code=YOUR_AUTH_CODE"
```

**응답:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "...",
  "expires_in": 21599,
  "scope": "..."
}
```

### 3. 사용자 정보 조회
```bash
curl "http://localhost:2501/kakao-authentication/user-info?access_token=YOUR_ACCESS_TOKEN"
```

**응답:**
```json
{
  "id": 123456789,
  "kakao_account": {
    "profile": {
      "nickname": "홍길동"
    },
    "email": "user@example.com"
  }
}
```

## 인증 플로우

1. **프론트엔드**: `/request-oauth-link`를 호출하여 Kakao 인증 URL 획득
2. **사용자**: 반환된 URL로 리다이렉트하여 Kakao 로그인 수행
3. **Kakao**: 인증 성공 시 `redirect_uri`로 인가 코드(`code`) 전달
4. **프론트엔드**: `/request-access-token-after-redirection?code={code}`로 액세스 토큰 요청
5. **백엔드**: Kakao API를 통해 액세스 토큰 발급 및 반환
6. **프론트엔드**: `/user-info?access_token={token}`으로 사용자 정보 조회

## 개발 원칙

- **DRY (Don't Repeat Yourself)**: 중복 코드 최소화
- **관심사의 분리**: Controller/Service/Config 명확한 역할 구분
- **의존성 역전 원칙**: Controller는 Service Interface에만 의존
- **환경 변수 기반 설정**: 하드코딩 금지, `.env` 파일 사용
- **명시적 에러 처리**: 각 계층에서 적절한 예외 처리 및 메시지 제공

## 주의사항

- `.env` 파일은 절대 Git에 커밋하지 마세요 (`.gitignore`에 포함됨)
- 프로덕션 환경에서는 CORS 설정을 특정 도메인으로 제한하세요
- Kakao API 사용량 제한을 고려하여 적절한 캐싱 전략을 추가할 수 있습니다
