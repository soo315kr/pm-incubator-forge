"""애플리케이션 설정 (sprint_1 - config)."""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경 변수 기반 설정."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "FastAPI Backend"
    debug: bool = False
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    # Notion 가이드: KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI_HOST
    kakao_client_id: Optional[str] = None
    kakao_redirect_uri_host: Optional[str] = None
    # 기존: KAKAO_REST_API_KEY, KAKAO_REDIRECT_URI (둘 다 지원)
    kakao_rest_api_key: Optional[str] = None
    kakao_redirect_uri: Optional[str] = None
    kakao_client_secret: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    """설정 싱글톤."""
    return Settings()
