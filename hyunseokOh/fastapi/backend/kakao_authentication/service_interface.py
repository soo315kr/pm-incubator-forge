"""Service interfaces for Kakao authentication. Controllers depend only on these."""

from abc import ABC, abstractmethod
from typing import Any


class OAuthLinkServiceInterface(ABC):
    """Interface for generating Kakao OAuth authorization URL."""

    @abstractmethod
    def get_authorization_url(self) -> str:
        """Return Kakao OAuth authorization URL with required parameters."""
        ...


class TokenExchangeServiceInterface(ABC):
    """Interface for exchanging authorization code for access token."""

    @abstractmethod
    def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        """Exchange authorization code for access_token, refresh_token, expires_in. Raises on error."""
        ...


class UserInfoServiceInterface(ABC):
    """Interface for fetching Kakao user info with access token."""

    @abstractmethod
    def get_user_info(self, access_token: str) -> dict[str, Any]:
        """Return Kakao user info (id, nickname, email etc.). Raises on invalid/expired token."""
        ...
