"""
Kakao 인증 서비스 인터페이스

Controller는 이 인터페이스에만 의존합니다.
"""
from abc import ABC, abstractmethod
from models.kakao_authentication import (
    OAuthLinkResponse,
    AccessTokenResponse,
    KakaoUserInfo,
)


class KakaoAuthenticationServiceInterface(ABC):
    """Kakao 인증 서비스 인터페이스"""

    @abstractmethod
    def generate_oauth_link(self) -> OAuthLinkResponse:
        pass

    @abstractmethod
    def request_access_token(self, code: str) -> AccessTokenResponse:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> KakaoUserInfo:
        pass
