"""Application settings loaded from environment variables."""
import os
from typing import Optional


class KakaoOAuthSettings:
    """Kakao OAuth configuration settings."""
    
    def __init__(self):
        self._client_id: Optional[str] = None
        self._redirect_uri: Optional[str] = None
        self._client_secret: Optional[str] = None
        self._initialized = False
    
    def _ensure_initialized(self) -> None:
        """Ensure settings are loaded from environment variables."""
        # Always reload from environment to ensure latest values
        self._client_id = os.getenv("KAKAO_CLIENT_ID", "")
        self._redirect_uri = os.getenv("KAKAO_REDIRECT_URI", "")
        self._client_secret = os.getenv("KAKAO_CLIENT_SECRET")
        self._initialized = True
    
    @property
    def client_id(self) -> str:
        """Get client ID from environment variables."""
        self._ensure_initialized()
        return self._client_id or ""
    
    @property
    def redirect_uri(self) -> str:
        """Get redirect URI from environment variables."""
        self._ensure_initialized()
        return self._redirect_uri or ""
    
    @property
    def client_secret(self) -> Optional[str]:
        """Get client secret from environment variables."""
        self._ensure_initialized()
        return self._client_secret
    
    def validate(self) -> None:
        """Validate that required settings are present."""
        self._ensure_initialized()
        if not self._client_id:
            raise ValueError("KAKAO_CLIENT_ID environment variable is required")
        if not self._redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI environment variable is required")


# Global settings instance (lazy initialization)
kakao_oauth_settings = KakaoOAuthSettings()
