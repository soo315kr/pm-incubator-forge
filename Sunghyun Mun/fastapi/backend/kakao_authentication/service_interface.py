"""
Kakao OAuth Service Interface.
Controller는 이 인터페이스에만 의존하며, 구현체에 직접 의존하지 않는다.
"""
from abc import ABC, abstractmethod

from kakao_authentication.schemas import KakaoUserInfo, OAuthLinkResponse, TokenResponse


class KakaoOAuthServiceInterface(ABC):
    """Kakao OAuth 인증 URL 생성 및 토큰 발급 서비스 인터페이스."""

    @abstractmethod
    def get_oauth_authorize_url(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 페이지 URL을 생성하여 반환한다."""
        ...

    @abstractmethod
    def request_access_token_after_redirection(self, code: str) -> TokenResponse:
        """
        인가 코드(code)로 액세스 토큰을 요청하고,
        발급된 토큰으로 사용자 정보를 조회하여 함께 반환한다.
        """
        ...
