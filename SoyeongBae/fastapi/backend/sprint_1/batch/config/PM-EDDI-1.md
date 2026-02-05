# PM-EDDI-1: 환경 변수 로딩을 위한 config/env 초기화

- **feature_id**: PM-EDDI-1
- **domain**: config

## Success criteria

- [x] 애플리케이션 시작 시 `.env` 파일이 1회 로드된다.
- [x] 환경 변수 로딩 책임은 config 패키지에 명시적으로 위치한다.
- [x] Service 및 Controller에서는 `.env` 파일을 직접 로드하지 않는다.
- [x] 환경 변수 로딩 여부는 애플리케이션 전역에서 일관되게 보장된다.

## Todos

- [x] python-dotenv 의존성 추가
- [x] config/env.py 생성 및 load_env 함수 구현
- [x] 애플리케이션 엔트리포인트에서 load_env 호출
