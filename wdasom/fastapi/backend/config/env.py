from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_LOADED = False


def load_env() -> None:
    """
    애플리케이션 시작 시 단 한 번만 .env 파일을 로드한다.

    - 로딩 책임은 config 패키지에만 둔다.
    - Service / Controller 등 다른 레이어에서는 이 함수를 직접 호출하지 않고,
      애플리케이션 엔트리포인트에서만 호출하도록 한다.
    """
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    # 기본적으로 backend 루트(.env)를 바라보도록 설정
    backend_root = Path(__file__).resolve().parents[1]
    env_path = backend_root / ".env"

    if env_path.is_file():
        load_dotenv(dotenv_path=env_path, override=False)
    else:
        # 그래도 시스템 환경변수는 사용할 수 있도록 한다.
        load_dotenv(override=False)

    _ENV_LOADED = True


def get_env(key: str, default: str | None = None) -> str:
    """
    환경 변수를 읽기 위한 헬퍼 함수.
    개별 레이어에서 os.getenv 대신 이 함수를 사용하면 의미가 더 명확해진다.
    """
    return os.getenv(key, default)  # type: ignore[return-value]

