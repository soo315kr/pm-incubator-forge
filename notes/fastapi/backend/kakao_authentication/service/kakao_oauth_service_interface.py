from abc import ABC, abstractmethod
from kakao_authentication.schemas.kakao_oauth import (
    KakaoAuthUrlResponse,
    KakaoTokenResponse,
    KakaoUserInfoResponse,
)


class KakaoOAuthServiceInterface(ABC):
    """Kakao OAuth Service Interface"""

    @abstractmethod
    def generate_auth_url(self) -> KakaoAuthUrlResponse:
        """Kakao 인증 URL 생성"""
        pass

    @abstractmethod
    async def request_access_token(self, code: str) -> KakaoTokenResponse:
        """인가 코드로 액세스 토큰 요청"""
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> KakaoUserInfoResponse:
        """액세스 토큰으로 사용자 정보 조회"""
        pass
