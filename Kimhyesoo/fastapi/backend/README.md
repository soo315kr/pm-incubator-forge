# Kakao Authentication API

FastAPI 기반 Kakao OAuth 인증 API입니다.

## 기능

- **PM-KHS-1**: 환경 변수 로딩 설정
- **PM-KHS-2**: Kakao 인증 URL 생성
- **PM-KHS-3**: Kakao 액세스 토큰 요청
- **PM-KHS-4**: Kakao 사용자 정보 조회

## 설치

```bash
pip install -r requirements.txt
```

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
KAKAO_CLIENT_ID=your_kakao_client_id
KAKAO_REDIRECT_URI=http://localhost:8000/kakao/callback
KAKAO_CLIENT_SECRET=your_kakao_client_secret
```

## 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload
```

## API 엔드포인트

### 1. 인증 URL 생성
```
GET /kakao-authentication/request-oauth-link
```

Kakao OAuth 인증 URL을 생성합니다.

**응답 예시:**
```json
{
  "auth_url": "https://kauth.kakao.com/oauth/authorize?client_id=..."
}
```

### 2. 액세스 토큰 요청
```
GET /kakao-authentication/request-access-token-after-redirection?code={인가코드}
```

인가 코드를 사용하여 액세스 토큰을 요청합니다.

**응답 예시:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "...",
  "expires_in": 21599,
  "refresh_token_expires_in": 5183999,
  "scope": "profile_nickname account_email"
}
```

### 3. 사용자 정보 조회 (토큰 + 사용자 정보 통합)
```
GET /kakao-authentication/get-user-info?code={인가코드}
```

인가 코드를 받아 액세스 토큰을 요청하고, 해당 토큰으로 사용자 정보를 조회합니다.

**응답 예시:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "...",
  "expires_in": 21599,
  "refresh_token_expires_in": 5183999,
  "scope": "profile_nickname account_email",
  "user_info": {
    "id": 123456789,
    "nickname": "사용자닉네임",
    "email": "user@example.com",
    "profile_image": "https://..."
  }
}
```

## 프로젝트 구조 (레이어별 분리)

```
backend/
├── config/                 # 설정
│   └── env.py
├── api/                    # HTTP 레이어 (컨트롤러/라우터)
│   └── kakao_authentication.py
├── services/               # 비즈니스 로직 레이어
│   ├── interfaces/        # 서비스 인터페이스
│   │   └── kakao_authentication.py
│   └── impl/              # 서비스 구현체
│       └── kakao_authentication.py
├── models/                 # 도메인/응답 모델
│   └── kakao_authentication.py
├── main.py
├── requirements.txt
└── README.md
```

## 아키텍처

- **api/**: 라우터만 두고, 요청/응답 처리만 담당
- **services/interfaces/**: 서비스 계약(인터페이스)
- **services/impl/**: 실제 비즈니스 로직·외부 API 호출
- **models/**: DTO·응답 모델

API 레이어는 Service Interface에만 의존하고, 새 도메인을 추가할 때도 같은 레이어에 파일만 추가하면 됩니다.
