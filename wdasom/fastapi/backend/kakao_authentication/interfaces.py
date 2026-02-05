from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import (
    KakaoOAuthUrlResponse,
    KakaoTokenAndUserResponse,
)


class KakaoAuthenticationService(ABC):
    """
    Kakao 인증 관련 Service 인터페이스.

    Controller는 이 인터페이스에만 의존하도록 한다.
    """

    @abstractmethod
    def build_oauth_authorize_url(self) -> KakaoOAuthUrlResponse:
        """사용자가 Kakao 로그인 페이지로 이동할 수 있는 인증 URL을 생성한다."""
        raise NotImplementedError

    @abstractmethod
    async def request_access_token_and_user_info(
        self,
        code: str,
    ) -> KakaoTokenAndUserResponse:
        """
        인가 코드(code)를 이용해 Kakao 액세스 토큰을 발급받고,
        발급받은 토큰으로 사용자 정보를 조회하여 함께 반환한다.
        """
        raise NotImplementedError

