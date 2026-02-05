"""
Kakao OAuth 설정. 환경 변수(.env)에서만 로드하며 코드에 하드코딩하지 않는다.
Controller/Service는 이 모듈을 통해 설정값을 사용한다.
"""

import os


def get_kakao_client_id() -> str | None:
    """KAKAO_CLIENT_ID 환경 변수 값. 없으면 None."""
    return os.getenv("KAKAO_CLIENT_ID")


def get_kakao_redirect_uri() -> str | None:
    """KAKAO_REDIRECT_URI 환경 변수 값. 없으면 None."""
    return os.getenv("KAKAO_REDIRECT_URI")


def get_kakao_client_secret() -> str | None:
    """KAKAO_CLIENT_SECRET 환경 변수 값. 없으면 None. (토큰 요청 시 선택 사용)"""
    return os.getenv("KAKAO_CLIENT_SECRET")
