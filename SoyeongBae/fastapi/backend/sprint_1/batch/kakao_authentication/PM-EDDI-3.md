# PM-EDDI-3: 인가 코드(code)를 받아 Kakao 액세스 토큰 요청

- **feature_id**: PM-EDDI-3
- **domain**: kakao_authentication

## Success criteria

- [x] 사용자는 Kakao 인증 후 발급된 인가 코드(code)를 통해 액세스 토큰을 정상적으로 발급받을 수 있다.
- [x] 액세스 토큰 발급 시 Kakao OAuth 기준(client_id, redirect_uri, code, grant_type 등)에 맞춰 요청이 처리된다.
- [x] 발급된 액세스 토큰은 바로 API 요청에 사용 가능하며, 토큰 만료 시간 및 리프레시 토큰도 포함된다.
- [x] 잘못된 인가 코드나 파라미터 누락 시 적절한 오류 메시지를 반환한다.
- [x] 인증 URL 생성 로직은 Layered Architecture를 따르며 Controller는 Service Interface에만 의존한다.
- [x] Service Interface와 구현체는 명시적으로 분리되며, Controller는 구현체에 직접 의존하지 않는다.
- [x] Kakao OAuth 관련 설정값(client_id, redirect_uri)은 환경 변수(.env) 기반으로 로드되며 코드에 하드코딩되지 않는다.
- [x] Controller는 환경 변수, 기본값 결정, 인증 URL 구성 로직을 직접 다루지 않으며 요청 전달 및 응답 반환 역할만 수행한다.

## Todos

- [x] `GET /kakao-authentication/request-access-token-after-redirection` API 구현 및 필수 파라미터 검증
- [x] Service Interface 설계 및 구현체 작성
- [x] Kakao 토큰 서버로 요청 로직 구현
- [x] 발급된 액세스 토큰 및 리프레시 토큰 반환 처리
- [x] 예외 처리 (잘못된 코드, 파라미터 누락 등)

## API

- **GET** `/kakao-authentication/request-access-token-after-redirection?code={인가코드}`
- **성공**: `200` + `access_token`, `token_type`, `refresh_token`, `expires_in`, `refresh_token_expires_in`, `scope`
- **실패**: `400` + `detail` (code 누락, 잘못된 코드, 설정 누락 등)

## 환경 변수

- `KAKAO_CLIENT_ID`, `KAKAO_REDIRECT_URI` (필수)
- `KAKAO_CLIENT_SECRET` (선택, 보안 강화 시)
