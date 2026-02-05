"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend 루트: app/config/settings.py -> config -> app -> backend (실행 위치와 무관하게 .env 경로 고정)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _BACKEND_ROOT / ".env"


class Settings(BaseSettings):
    """App settings. Values are read from env and backend 루트 .env 파일."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = Field(default="backend", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    environment: Literal["local", "dev", "staging", "prod"] = Field(
        default="local", description="Environment"
    )

    # Kakao OAuth (.env: KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI)
    kakao_client_id: str = Field(default="", description="Kakao client ID (REST API key)")
    kakao_client_secret: str = Field(default="", description="Kakao client secret")
    kakao_redirect_uri: str = Field(default="", description="Kakao redirect URI")
    kakao_authorize_url: str = Field(
        default="https://kauth.kakao.com/oauth/authorize",
        description="Kakao OAuth authorize URL",
    )
    kakao_token_url: str = Field(
        default="https://kauth.kakao.com/oauth/token",
        description="Kakao OAuth token URL",
    )
    kakao_user_info_url: str = Field(
        default="https://kapi.kakao.com/v2/user/me",
        description="Kakao user info API URL",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


# Convenience instance for direct import
settings = get_settings()
