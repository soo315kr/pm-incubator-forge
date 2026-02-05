"""
Kakao 인증 Service 인터페이스.
Controller는 이 인터페이스에만 의존하며, 구현체에 직접 의존하지 않는다.
"""
from abc import ABC, abstractmethod

from kakao_authentication.models.schemas import OAuthLinkResponse, TokenAndUserResponse


class KakaoAuthServiceInterface(ABC):
    """Kakao 인증 Service 인터페이스 (PM-EDDI-2, PM-EDDI-3, PM-EDDI-4)."""

    @abstractmethod
    def get_oauth_link(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 URL을 생성하여 반환 (PM-EDDI-2)."""
        ...

    @abstractmethod
    def request_access_token_and_user(self, code: str) -> TokenAndUserResponse:
        """
        인가 코드로 액세스 토큰을 발급받고, 해당 토큰으로 사용자 정보를 조회하여 반환 (PM-EDDI-3 + PM-EDDI-4).
        """
        ...
