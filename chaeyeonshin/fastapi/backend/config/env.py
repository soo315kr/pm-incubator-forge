"""환경 변수 로딩. 애플리케이션 시작 시 1회 호출한다."""
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """프로젝트 루트의 .env 파일을 1회 로드한다. 전역 os.environ에 반영된다."""
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    load_dotenv(env_path, override=False)
