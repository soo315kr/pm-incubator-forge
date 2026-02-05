"""Kakao 인증 Service Interface. Controller는 이 인터페이스에만 의존한다."""

from abc import ABC, abstractmethod

from kakao_authentication.dto import TokenWithUserResponse


class KakaoAuthServiceInterface(ABC):
    """Kakao OAuth 인증 URL 생성, 토큰 교환 및 사용자 정보 조회 서비스 인터페이스."""

    @abstractmethod
    def get_authorization_url(self) -> str:
        """
        Kakao OAuth 인증 URL을 생성하여 반환한다.
        client_id, redirect_uri, response_type 등 필수 파라미터를 포함한다.

        Returns:
            Kakao 인증 페이지로 이동할 URL

        Raises:
            KakaoOAuthConfigError: 필수 설정(client_id, redirect_uri)이 누락된 경우
        """
        ...

    @abstractmethod
    def exchange_code_for_tokens(self, code: str) -> TokenWithUserResponse:
        """
        인가 코드(code)로 토큰을 발급받고, 발급된 액세스 토큰으로 사용자 정보를 조회하여 함께 반환한다.

        Args:
            code: Kakao 인증 후 리다이렉트로 받은 인가 코드

        Returns:
            발급된 액세스 토큰·리프레시 토큰 및 Kakao 사용자 정보(사용자 ID, 닉네임, 이메일 등)

        Raises:
            KakaoOAuthConfigError: 필수 설정 누락
            KakaoTokenError: 잘못된 코드, 파라미터 누락, Kakao 서버 오류 등
            KakaoUserInfoError: 유효하지 않거나 만료된 토큰, 사용자 정보 API 오류 등
        """
        ...
