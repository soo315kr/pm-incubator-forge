"""Kakao 인증 Service Interface (PM-EDDI-2). Controller는 이 인터페이스에만 의존."""

from typing import Protocol


class KakaoAuthServiceProtocol(Protocol):
    """Kakao OAuth 인증 URL 생성 등 서비스 인터페이스."""

    def get_oauth_authorization_url(self) -> str:
        """Kakao OAuth 인증 URL을 반환한다."""
        ...
