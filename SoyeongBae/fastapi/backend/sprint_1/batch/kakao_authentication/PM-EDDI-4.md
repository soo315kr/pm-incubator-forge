# PM-EDDI-4: 발급 받은 액세스 토큰으로 Kakao 사용자 정보 조회

- **feature_id**: PM-EDDI-4
- **domain**: kakao_authentication

## Success criteria

- [x] 사용자는 PM-EDDI-3에서 발급받은 Kakao 액세스 토큰을 통해 자신의 Kakao 계정 정보를 조회할 수 있다.
- [x] 조회 가능한 정보에는 사용자 ID, 닉네임, 이메일(동의 시) 등이 포함된다.
- [x] 액세스 토큰이 유효하지 않거나 만료된 경우, 적절한 오류 메시지가 반환된다.
- [x] PM-EDDI-3 Service 로직 내에서 호출되어, 발급된 액세스 토큰과 함께 사용자 정보를 반환하도록 연동된다.
- [x] 조회된 사용자 정보는 Service 로직에서 바로 활용 가능하다.
- [x] 사용자 정보 조회 로직은 Layered Architecture를 준수하며, Controller는 Service 인터페이스만 호출한다.

## Todos

- [x] 액세스 토큰 유효성 검증
- [x] Kakao API 요청 로직 구현
- [x] 응답 데이터 파싱 및 모델 매핑
- [x] 예외 처리 (유효하지 않은 토큰, API 오류 등)
- [x] 반환 값 정의 및 문서화 (PM-EDDI-3 토큰 발급 결과와 통합)

## 연동 방식

- **GET** `/kakao-authentication/request-access-token-after-redirection?code={인가코드}` 응답에 `user` 객체가 포함된다.
- **user** 필드: `id`, `nickname`, `email`, `profile_image_url`, `thumbnail_image_url` (동의/미동의에 따라 null 가능)
- 토큰 발급 후 Service 내부에서 Kakao `GET /v2/user/me`를 호출하여 사용자 정보를 조회한 뒤, 토큰과 함께 한 번에 반환한다.

## 예외

- 액세스 토큰이 유효하지 않거나 만료된 경우: `400` + `"액세스 토큰이 유효하지 않거나 만료되었습니다. 다시 로그인해 주세요."`
- 사용자 정보 API 오류: `400` + `detail` 메시지
