"""
Kakao 인증 Service Interface (Layered Architecture).
Controller는 이 인터페이스에만 의존하며, 구현체에 직접 의존하지 않는다.
"""

from abc import ABC, abstractmethod

from kakao_authentication.schemas import AccessTokenResult, OAuthLinkResponse


class KakaoAuthenticationServiceInterface(ABC):
    """Kakao 인증 서비스 인터페이스"""

    @abstractmethod
    def get_oauth_authorization_url(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 URL을 생성하여 반환한다. (PM-EDDI-2)"""
        ...

    @abstractmethod
    def request_access_token_after_redirection(self, code: str) -> AccessTokenResult:
        """
        인가 코드(code)로 Kakao 액세스 토큰을 요청하고, 발급된 토큰으로 사용자 정보를 조회하여 반환한다.
        (PM-EDDI-3, PM-EDDI-4)
        """
        ...
