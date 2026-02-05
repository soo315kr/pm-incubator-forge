"""Kakao OAuth 도메인 예외."""


class KakaoOAuthConfigError(Exception):
    """Kakao OAuth 필수 설정값이 누락되었을 때 발생."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class KakaoOAuthTokenError(Exception):
    """인가 코드 교환 실패 또는 잘못된 코드/파라미터로 토큰 발급 실패 시 발생."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class KakaoUserInfoError(Exception):
    """액세스 토큰이 유효하지 않거나 만료되어 사용자 정보 조회 실패 시 발생."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
