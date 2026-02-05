"""애플리케이션 시작 시 .env 1회 로드 (PM-EDDI-1)."""

from pathlib import Path

from dotenv import load_dotenv

_loaded = False


def load_env() -> None:
    """`.env` 파일을 1회 로드한다. config 패키지 전용 책임."""
    global _loaded
    if _loaded:
        return
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
    _loaded = True
