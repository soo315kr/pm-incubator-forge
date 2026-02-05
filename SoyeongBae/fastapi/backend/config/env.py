"""환경 변수 로딩. .env 파일은 config 패키지에서만 1회 로드한다."""

from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """
    .env 파일을 1회 로드한다.
    애플리케이션 엔트리포인트에서 1회만 호출하며,
    Service/Controller에서는 호출하지 않는다.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
