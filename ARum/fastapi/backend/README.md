# Kakao Authentication API (FastAPI)

PM-EDDI-1 ~ PM-EDDI-4 전략에 따른 Kakao OAuth 인증 백엔드입니다.

## 설정

1. 가상환경 생성 및 활성화 후 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

2. 프로젝트 루트(`backend`)에 `.env` 파일 생성:
   ```
   KAKAO_CLIENT_ID=your_rest_api_key
   KAKAO_REDIRECT_URI=http://localhost:8000/callback
   ```

## 실행

```bash
uvicorn main:app --reload
```

- API 문서: http://localhost:8000/docs

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/kakao-authentication/request-oauth-link` | Kakao 인증 URL 생성 (PM-EDDI-2) |
| GET | `/kakao-authentication/request-access-token-after-redirection?code=...` | 인가 코드로 액세스 토큰 발급 + 사용자 정보 조회 (PM-EDDI-3, PM-EDDI-4) |

환경 변수(`KAKAO_CLIENT_ID`, `KAKAO_REDIRECT_URI`)는 config에서 로드되며, Controller/Service는 `.env`를 직접 로드하지 않습니다 (PM-EDDI-1).
