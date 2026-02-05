"""Kakao 인증 도메인 예외."""


class KakaoAuthenticationError(Exception):
    """Kakao 인증 관련 기본 예외."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class KakaoConfigError(KakaoAuthenticationError):
    """필수 설정(client_id, redirect_uri 등) 누락."""

    def __init__(self, message: str = "Kakao OAuth 설정이 올바르지 않습니다."):
        super().__init__(message, status_code=500)


class KakaoInvalidRequestError(KakaoAuthenticationError):
    """잘못된 요청(파라미터 누락, 잘못된 코드 등)."""

    def __init__(self, message: str = "잘못된 요청입니다."):
        super().__init__(message, status_code=400)


class KakaoTokenError(KakaoAuthenticationError):
    """토큰 발급/검증 실패."""

    def __init__(self, message: str = "토큰 발급에 실패했습니다."):
        super().__init__(message, status_code=400)


class KakaoUserInfoError(KakaoAuthenticationError):
    """사용자 정보 조회 실패."""

    def __init__(self, message: str = "사용자 정보를 조회할 수 없습니다."):
        super().__init__(message, status_code=401)
