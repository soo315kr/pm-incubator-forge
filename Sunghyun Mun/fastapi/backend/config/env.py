"""
환경 변수 로딩 책임을 config 패키지에 명시적으로 위치시킨다.
애플리케이션 시작 시 .env 파일을 1회 로드한다.
"""
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env(env_file: Optional[str] = ".env") -> None:
    """
    .env 파일을 로드하여 환경 변수로 주입한다.
    env_file이 None이면 기본 .env를 사용하며,
    프로젝트 루트 기준 경로에서 .env를 찾는다.
    """
    if env_file is None:
        env_file = ".env"
    base = Path(__file__).resolve().parent.parent
    load_dotenv(dotenv_path=base / env_file, override=False)
