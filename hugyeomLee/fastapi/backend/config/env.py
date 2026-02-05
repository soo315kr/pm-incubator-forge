"""
환경 변수 로딩을 위한 config/env 초기화 (PM-EDDI-1)
애플리케이션 시작 시 .env 파일이 1회 로드되며, 환경 변수 로딩 책임은 config 패키지에 위치한다.
"""

from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env(env_file: Optional[str] = ".env") -> None:
    """
    .env 파일을 로드하여 환경 변수를 주입한다.
    애플리케이션 전역에서 일관되게 1회만 호출한다.

    Args:
        env_file: 로드할 .env 파일 경로. 기본값 ".env"
    """
    if env_file is None:
        return
    path = Path(env_file)
    if path.is_file():
        load_dotenv(path, override=False)
