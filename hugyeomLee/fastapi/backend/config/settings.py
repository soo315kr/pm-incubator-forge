"""
Kakao OAuth 설정. 환경 변수(.env) 기반으로 로드되며 코드에 하드코딩되지 않는다.
load_env() 호출 후 사용한다.
"""

import os
from typing import Optional


def get_kakao_client_id() -> str:
    value = os.getenv("KAKAO_CLIENT_ID")
    if not value:
        raise ValueError("KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다.")
    return value


def get_kakao_redirect_uri() -> str:
    value = os.getenv("KAKAO_REDIRECT_URI")
    if not value:
        raise ValueError("KAKAO_REDIRECT_URI 환경 변수가 설정되지 않았습니다.")
    return value


def get_kakao_client_secret() -> Optional[str]:
    return os.getenv("KAKAO_CLIENT_SECRET")
