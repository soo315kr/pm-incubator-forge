"""Kakao 인증 도메인 예외. 잘못된 요청·누락된 파라미터 시 사용."""


class KakaoOAuthConfigError(Exception):
    """Kakao OAuth 필수 설정(client_id, redirect_uri) 누락 또는 잘못된 경우."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class KakaoTokenError(Exception):
    """인가 코드로 토큰 교환 실패(잘못된 코드, 파라미터 누락, Kakao 서버 오류 등)."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class KakaoUserInfoError(Exception):
    """액세스 토큰으로 사용자 정보 조회 실패(유효하지 않음, 만료, API 오류 등)."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
