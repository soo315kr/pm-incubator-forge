"""Kakao 인증 Service 인터페이스. Controller는 이 인터페이스에만 의존한다."""

from abc import ABC, abstractmethod

from kakao_authentication.schemas import OAuthLinkResponse, TokenWithUserResponse


class KakaoAuthenticationServiceInterface(ABC):
    """Kakao OAuth 인증 URL 생성 및 토큰·사용자 정보 조회 서비스 인터페이스."""

    @abstractmethod
    def get_oauth_link(self) -> OAuthLinkResponse:
        """Kakao 인증 페이지 URL을 생성하여 반환한다."""
        ...

    @abstractmethod
    def request_access_token_after_redirection(self, code: str) -> TokenWithUserResponse:
        """인가 코드로 액세스 토큰을 발급받고, 해당 토큰으로 사용자 정보를 조회하여 함께 반환한다."""
        ...
