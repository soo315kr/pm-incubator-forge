# Backend

FastAPI 기반 백엔드 (sprint_1: config, kakao_authentication).

## 구조

- `config/` — 앱 설정 (pydantic-settings, .env 자동 로드)
- `kakao_authentication/` — 카카오 OAuth (router, service, templates)
- `strategy/` — 전략 YAML
- `test-strategy/`, `tmp/` — 테스트·임시

## 실행

### 방법 1: run.bat (Windows, 권장)

`run.bat` 더블클릭 또는 터미널에서:

```cmd
run.bat
```

서버가 **http://localhost:33333** 에서 실행됩니다. 에러가 나면 창이 닫히지 않고 메시지를 볼 수 있습니다.

### 방법 2: 터미널에서 직접

```bash
# 의존성 설치 (최초 1회)
pip install -r requirements.txt
# 또는: py -m pip install -r requirements.txt

# .env 수정 후 (KAKAO_REST_API_KEY, KAKAO_REDIRECT_URI)

# 서버 실행 (33333 포트)
py -m uvicorn main:app --port 33333 --host 0.0.0.0

# 또는 (main.py에 서버 실행 코드 포함)
py -m main
```

**Windows PowerShell:** `python -m main` 대신 **`py -m main`** 을 사용하세요. `python`이 스토어용 스텁이면 "Python"만 출력되고 서버가 안 뜹니다.

**포트가 이미 사용 중(10048)** 이면, 기존 서버를 Ctrl+C로 종료하거나:

```cmd
netstat -ano | findstr :33333
taskkill /PID <나온_PID> /F
```

## 환경 변수

`.env.example` 참고. 카카오 로그인 사용 시 `KAKAO_REST_API_KEY`, `KAKAO_REDIRECT_URI` 설정.

### 카카오 "Bad client credentials" 오류 시

1. **카카오 개발자 콘솔** (https://developers.kakao.com) → 내 애플리케이션 → 해당 앱
2. **앱 키**  
   - **REST API 키**가 `.env`의 `KAKAO_REST_API_KEY`(또는 `KAKAO_CLIENT_ID`)와 **완전히 동일**한지 확인.
3. **카카오 로그인** → **Redirect URI**  
   - `http://localhost:33333/kakao-authentication/request-access-token-after-redirection` 을 **그대로** 등록 (끝 슬래시 없음, http/https 일치).
4. **보안** → **Client Secret**  
   - "Client Secret 사용"이 **사용함**이면, 여기서 보이는 **Client Secret** 값을 `.env`에 추가:
   ```env
   KAKAO_CLIENT_SECRET=발급받은_시크릿_값
   ```
   - 사용 안 함이면 이 변수는 비워두면 됨.
5. `.env` 수정 후 서버를 **재시작** (Ctrl+C 후 `py -m main` 다시 실행).
