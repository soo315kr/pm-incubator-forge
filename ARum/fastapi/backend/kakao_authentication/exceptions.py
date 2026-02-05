"""Kakao 인증 도메인 예외. 적절한 HTTP 응답으로 변환된다."""


class KakaoAuthenticationError(Exception):
    """Kakao 인증 관련 기본 예외."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class MissingConfigError(KakaoAuthenticationError):
    """필수 설정(환경 변수) 누락."""

    def __init__(self, message: str = "Kakao OAuth 설정이 누락되었습니다."):
        super().__init__(message, status_code=503)


class InvalidRequestError(KakaoAuthenticationError):
    """잘못된 요청(파라미터 누락, 잘못된 값 등)."""

    def __init__(self, message: str = "요청 파라미터가 올바르지 않습니다."):
        super().__init__(message, status_code=400)


class KakaoApiError(KakaoAuthenticationError):
    """Kakao API 호출 실패(토큰/사용자 정보)."""

    def __init__(self, message: str = "Kakao 인증 처리에 실패했습니다.", status_code: int = 502):
        super().__init__(message, status_code)
