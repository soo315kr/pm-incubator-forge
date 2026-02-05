"""
PM-EDDI-1: 환경 변수 로딩을 위한 config/env 초기화
- 애플리케이션 시작 시 .env 파일이 1회 로드된다.
- Service 및 Controller에서는 .env 파일을 직접 로드하지 않는다.
"""
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os


_env_loaded = False


def load_env() -> None:
    """애플리케이션 전역에서 .env를 1회 로드한다. 엔트리포인트(main)에서만 호출한다."""
    global _env_loaded
    if not _env_loaded:
        # 실행 경로와 무관하게 프로젝트 루트(backend/)의 .env를 로드
        backend_root = Path(__file__).resolve().parent.parent
        load_dotenv(dotenv_path=backend_root / ".env")
        _env_loaded = True


@dataclass(frozen=True)
class KakaoConfig:
    """Kakao OAuth 관련 설정. 환경 변수 기반, 코드에 하드코딩되지 않는다."""

    client_id: str
    redirect_uri: str

    @classmethod
    def from_env(cls) -> "KakaoConfig":
        client_id = os.getenv("KAKAO_CLIENT_ID") or ""
        redirect_uri = os.getenv("KAKAO_REDIRECT_URI") or ""
        return cls(client_id=client_id, redirect_uri=redirect_uri)


def get_kakao_config() -> KakaoConfig:
    """Kakao OAuth 설정을 반환한다. load_env() 호출 후 사용해야 한다."""
    return KakaoConfig.from_env()
