"""환경 변수 로딩. config 패키지에서 1회 로드 책임을 가짐."""

from dotenv import load_dotenv

_env_loaded = False


def load_env(env_file: str | None = ".env") -> None:
    """애플리케이션 전역에서 .env 파일을 1회 로드한다."""
    global _env_loaded
    if _env_loaded:
        return
    load_dotenv(env_file)
    _env_loaded = True
