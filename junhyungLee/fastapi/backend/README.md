# Backend

PM-EDDI 스펙 기반 FastAPI 백엔드 (config, kakao_authentication).

## 구조

- `config/` — 환경 변수 로딩 (PM-EDDI-1)
- `kakao_authentication/` — Kakao OAuth 인증 (PM-EDDI-2, 3, 4)
  - `config/` — Kakao 관련 설정
  - `controller/` — API 라우트
  - `models/` — 요청/응답 모델
  - `service/` — 비즈니스 로직 (Interface + 구현체)
- `strategy/` — 기능 스펙 YAML

## 실행

**방법 1 (권장)** — 스크립트 한 번에 실행:

```powershell
cd backend
.\run.ps1
```

또는 `run.bat` 더블클릭.

**방법 2** — 수동:

```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

서버가 뜬 뒤 브라우저에서: http://localhost:8000/kakao-authentication/request-oauth-link

## 환경 변수

`.env` 파일에 Kakao OAuth 설정 등 필요 시 추가 (PM-EDDI-1에서 1회 로드).
