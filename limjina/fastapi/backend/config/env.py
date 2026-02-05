"""
환경 변수 로딩 책임을 담당하는 config 패키지.
애플리케이션 시작 시 .env 파일을 1회 로드한다.
"""
from pathlib import Path

from dotenv import load_dotenv


_env_loaded = False


def load_env(env_file: str | None = ".env") -> None:
    """
    .env 파일을 1회 로드한다.
    이미 로드된 경우 재로드하지 않으며, 애플리케이션 전역에서 일관되게 보장된다.

    Args:
        env_file: 로드할 env 파일 경로. 기본값 ".env"
    """
    global _env_loaded
    if _env_loaded:
        return
    path = Path(env_file)
    if path.exists():
        load_dotenv(path)
    _env_loaded = True
