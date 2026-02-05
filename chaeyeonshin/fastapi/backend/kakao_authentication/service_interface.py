"""Kakao 인증 Service Interface. Controller는 이 인터페이스에만 의존한다."""
from abc import ABC, abstractmethod

from kakao_authentication.schemas import OAuthLinkResponse, TokenAndUserResponse


class KakaoAuthServiceInterface(ABC):
    """Kakao OAuth 인증 URL 생성 및 토큰·사용자정보 조회 서비스 인터페이스."""

    @abstractmethod
    def get_oauth_link(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 URL을 생성하여 반환한다."""
        ...

    @abstractmethod
    def exchange_code_for_token_and_user(self, code: str) -> TokenAndUserResponse:
        """인가 코드를 액세스 토큰으로 교환하고, 해당 토큰으로 사용자 정보를 조회하여 함께 반환한다."""
        ...
