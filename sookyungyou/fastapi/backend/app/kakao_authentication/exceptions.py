"""Kakao 인증 도메인 예외."""


class KakaoAuthenticationError(Exception):
    """Kakao 인증 관련 기본 예외."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InvalidOAuthConfigError(KakaoAuthenticationError):
    """필수 OAuth 설정(client_id, redirect_uri) 누락 또는 잘못된 경우."""
    def __init__(self, message: str = "Kakao OAuth 설정이 올바르지 않습니다. client_id, redirect_uri를 확인하세요."):
        super().__init__(message, status_code=503)


class InvalidAuthorizationCodeError(KakaoAuthenticationError):
    """잘못된 인가 코드 또는 파라미터 누락."""
    def __init__(self, message: str = "인가 코드가 유효하지 않거나 만료되었습니다."):
        super().__init__(message, status_code=400)


class InvalidAccessTokenError(KakaoAuthenticationError):
    """유효하지 않거나 만료된 액세스 토큰."""
    def __init__(self, message: str = "액세스 토큰이 유효하지 않거나 만료되었습니다."):
        super().__init__(message, status_code=401)


class KakaoApiError(KakaoAuthenticationError):
    """Kakao API 호출 실패."""
    def __init__(self, message: str = "Kakao API 요청에 실패했습니다.", status_code: int = 502):
        super().__init__(message, status_code)
