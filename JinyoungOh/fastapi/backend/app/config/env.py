"""
환경 변수 로딩 책임을 갖는 config 패키지 모듈.
애플리케이션 시작 시 .env 파일을 1회 로드한다.
"""
from pathlib import Path

from dotenv import load_dotenv

_loaded = False


def load_env() -> None:
    """
    .env 파일을 1회 로드한다.
    프로젝트 루트(backend) 기준으로 .env를 찾는다.
    이미 로드된 경우 재로드하지 않는다.
    """
    global _loaded
    if _loaded:
        return

    # backend 디렉터리 기준 .env 경로 (main.py 실행 위치 기준)
    root = Path(__file__).resolve().parent.parent.parent
    env_path = root / ".env"
    load_dotenv(dotenv_path=env_path)
    _loaded = True
