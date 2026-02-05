"""Kakao 인증 Service Interface. Controller는 이 인터페이스에만 의존한다."""

from abc import ABC, abstractmethod

from app.kakao_authentication.schemas import OAuthLinkResponse, TokenWithUserResponse


class KakaoAuthenticationServiceInterface(ABC):
    """Kakao 인증 서비스 인터페이스 (PM-EDDI-2, 3, 4)."""

    @abstractmethod
    def get_oauth_link(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 URL을 생성하여 반환한다 (PM-EDDI-2)."""
        ...

    @abstractmethod
    def exchange_code_for_token_with_user(self, code: str) -> TokenWithUserResponse:
        """인가 코드로 액세스 토큰을 발급받고, 해당 토큰으로 사용자 정보를 조회하여 반환한다 (PM-EDDI-3 + PM-EDDI-4)."""
        ...
