# Kakao OAuth Backend

PM-EDDI-1 ~ PM-EDDI-4 요구사항에 따른 Kakao 인증 백엔드 (FastAPI).  
**app 패키지 없이** 루트에서 `config`·`kakao_authentication`만 사용합니다.

## 구조

- **config/** — 환경 변수 로딩 (`.env` 1회 로드, PM-EDDI-1)
- **kakao_authentication/** — Kakao OAuth 인증
  - **config/** — Kakao 인증 설정
  - **controller/** — API 라우터 (PM-EDDI-2, PM-EDDI-3)
  - **models/** — 요청/응답 스키마 (PM-EDDI-3·4 통합 반환값)
  - **service/** — Service 인터페이스 및 구현체
- **test-strategy/** — 기능 요구사항 YAML (PM-EDDI-1~4)

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/kakao-authentication/request-oauth-link` | Kakao OAuth 인증 URL 반환 (PM-EDDI-2) |
| GET | `/kakao-authentication/request-access-token-after-redirection?code=...` | 인가 코드로 토큰·사용자 정보 반환 (PM-EDDI-3 + PM-EDDI-4) |

## 환경 변수 (.env)

```
KAKAO_CLIENT_ID=your_rest_api_key
KAKAO_REDIRECT_URI=https://your-domain/callback
```

## 실행

```bash
pip install -r requirements.txt
uvicorn main:application --reload
```
