"""Kakao OAuth 도메인 설정. 환경 변수(.env) 기반."""

import os

from kakao_authentication.models.exceptions import KakaoConfigError


def get_client_id() -> str:
    value = os.environ.get("KAKAO_CLIENT_ID") or os.environ.get("KAKAO_REST_API_KEY")
    if not value or not value.strip():
        raise KakaoConfigError("KAKAO_CLIENT_ID(또는 KAKAO_REST_API_KEY)가 설정되지 않았습니다.")
    return value.strip()


def get_redirect_uri() -> str:
    value = os.environ.get("KAKAO_REDIRECT_URI")
    if not value or not value.strip():
        raise KakaoConfigError("KAKAO_REDIRECT_URI가 설정되지 않았습니다.")
    return value.strip()
