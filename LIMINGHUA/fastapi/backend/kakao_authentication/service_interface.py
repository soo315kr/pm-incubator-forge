from abc import ABC, abstractmethod

from kakao_authentication.schemas import KakaoUserInfo, OAuthLinkResponse, TokenWithUserResponse


class KakaoAuthServiceInterface(ABC):
    """Service interface for Kakao OAuth. Controller depends only on this."""

    @abstractmethod
    def get_oauth_link(self) -> OAuthLinkResponse:
        """Build Kakao OAuth authorization URL with required parameters."""
        ...

    @abstractmethod
    def exchange_code_for_token_and_user(self, code: str) -> TokenWithUserResponse:
        """Exchange authorization code for access token and fetch user info."""
        ...
