import os
from pathlib import Path
from dotenv import load_dotenv

_env_loaded = False


def load_env() -> None:
    """
    애플리케이션 시작 시 .env 파일을 1회 로드한다.

    - 환경 변수 로딩 책임은 config 패키지에 명시적으로 위치한다.
    - Service 및 Controller에서는 .env 파일을 직접 로드하지 않는다.
    - 환경 변수 로딩 여부는 애플리케이션 전역에서 일관되게 보장된다.
    """
    global _env_loaded

    if _env_loaded:
        return

    env_path = Path(__file__).parent.parent / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    _env_loaded = True


def get_env(key: str, default: str | None = None) -> str | None:
    """환경 변수 값을 가져온다."""
    return os.getenv(key, default)


def get_kakao_client_id() -> str | None:
    """Kakao Client ID를 가져온다."""
    return get_env("KAKAO_CLIENT_ID")


def get_kakao_redirect_uri() -> str | None:
    """Kakao Redirect URI를 가져온다."""
    return get_env("KAKAO_REDIRECT_URI")
