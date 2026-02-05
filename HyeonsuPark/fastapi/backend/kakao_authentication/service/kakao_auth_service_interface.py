"""Kakao 인증 Service Interface. Controller는 이 인터페이스에만 의존한다."""

from abc import ABC, abstractmethod

from kakao_authentication.models import TokenWithUserResponse


class KakaoAuthServiceInterface(ABC):
    """Kakao OAuth 인증 서비스 인터페이스."""

    @abstractmethod
    def get_oauth_authorize_url(self) -> str:
        """Kakao OAuth 인증 URL을 생성하여 반환한다."""
        ...

    @abstractmethod
    def request_access_token_after_redirection(self, code: str) -> TokenWithUserResponse:
        """인가 코드로 액세스 토큰을 요청하고, 발급된 토큰과 사용자 정보를 반환한다."""
        ...
