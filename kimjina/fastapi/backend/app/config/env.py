"""환경 변수 로딩. 애플리케이션 시작 시 1회 호출하여 .env를 로드한다."""

from pathlib import Path

from dotenv import load_dotenv

# backend 루트(프로젝트 루트): app/config/env.py -> config -> app -> backend
_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent

_ENV_LOADED = False


def load_env(*, env_file: str | Path | None = None) -> None:
    """애플리케이션 전역에서 .env 파일을 1회 로드한다.

    .env 경로는 현재 작업 디렉터리가 아닌 backend 루트 기준으로 고정하여,
    uvicorn 등을 다른 디렉터리에서 실행해도 항상 읽을 수 있다.

    Service 및 Controller에서는 이 함수를 호출하지 않고,
    config 패키지의 settings를 통해 환경 변수를 사용한다.
    """
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    path = Path(env_file) if env_file is not None else _BACKEND_ROOT / ".env"
    if not path.is_absolute():
        path = _BACKEND_ROOT / path
    load_dotenv(path)
    _ENV_LOADED = True
