"""
Kakao OAuth Service Interface.
Controller는 이 인터페이스에만 의존하며, 구현체에 직접 의존하지 않는다.
"""
from abc import ABC, abstractmethod

from app.kakao_authentication.models import KakaoUserInfo, TokenResponse


class KakaoOAuthService(ABC):
    """Kakao OAuth 서비스 인터페이스."""

    @abstractmethod
    def get_oauth_link(self) -> str:
        """
        Kakao OAuth 인증 URL을 생성하여 반환한다.

        Returns:
            Kakao 인증 페이지로 이동할 URL

        Raises:
            KakaoOAuthConfigError: 필수 설정값(client_id, redirect_uri)이 없을 때
        """
        ...

    @abstractmethod
    def exchange_code_for_token(self, code: str) -> TokenResponse:
        """
        인가 코드(code)를 Kakao 토큰 서버에 보내 액세스 토큰을 발급받고,
        발급된 토큰으로 사용자 정보를 조회하여 함께 반환한다.

        Args:
            code: Kakao 인증 후 리다이렉트로 받은 인가 코드

        Returns:
            액세스 토큰, 리프레시 토큰, 만료 시간, 사용자 정보를 담은 TokenResponse

        Raises:
            KakaoOAuthConfigError: 필수 설정값이 없을 때
            KakaoOAuthTokenError: 잘못된 코드 또는 토큰 발급 실패 시
            KakaoUserInfoError: 토큰 발급 후 사용자 정보 조회 실패 시
        """
        ...

    @abstractmethod
    def get_user_info(self, access_token: str) -> KakaoUserInfo:
        """
        액세스 토큰으로 Kakao 사용자 정보를 조회한다.

        Args:
            access_token: PM-EDDI-3에서 발급받은 Kakao 액세스 토큰

        Returns:
            사용자 ID, 닉네임, 이메일(동의 시) 등을 담은 KakaoUserInfo

        Raises:
            KakaoUserInfoError: 토큰이 유효하지 않거나 만료된 경우, API 오류 시
        """
        ...
