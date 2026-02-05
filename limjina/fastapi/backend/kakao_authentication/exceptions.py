"""
Kakao 인증 도메인 예외.
PM-EDDI-2: 파라미터 누락, 잘못된 요청
PM-EDDI-3: 잘못된 코드, 파라미터 누락
PM-EDDI-4: 유효하지 않은 토큰, API 오류
"""
from typing import Optional


class KakaoAuthenticationError(Exception):
    """Kakao 인증 관련 기본 예외."""
    def __init__(self, message: str, detail: Optional[str] = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


class InvalidRequestError(KakaoAuthenticationError):
    """잘못된 요청 (PM-EDDI-2: 파라미터 누락, 잘못된 요청)."""
    pass


class MissingParameterError(KakaoAuthenticationError):
    """필수 파라미터 누락 (PM-EDDI-2, PM-EDDI-3)."""
    pass


class InvalidAuthorizationCodeError(KakaoAuthenticationError):
    """잘못된 인가 코드 (PM-EDDI-3)."""
    pass


class InvalidTokenError(KakaoAuthenticationError):
    """유효하지 않거나 만료된 액세스 토큰 (PM-EDDI-4)."""
    pass


class KakaoApiError(KakaoAuthenticationError):
    """Kakao API 호출 오류 (PM-EDDI-3, PM-EDDI-4)."""
    def __init__(self, message: str, status_code: Optional[int] = None, detail: Optional[str] = None):
        self.status_code = status_code
        super().__init__(message, detail)
