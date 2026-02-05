"""Kakao OAuth settings from environment. Do not load .env here; assume load_env() was called at app startup."""

import os

KAKAO_AUTHORIZE_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


def get_kakao_client_id() -> str:
    value = os.getenv("KAKAO_CLIENT_ID", "").strip()
    if not value:
        raise ValueError("KAKAO_CLIENT_ID is not set")
    return value


def get_kakao_redirect_uri() -> str:
    value = os.getenv("KAKAO_REDIRECT_URI", "").strip()
    if not value:
        raise ValueError("KAKAO_REDIRECT_URI is not set")
    return value


def get_kakao_client_secret() -> str:
    return os.getenv("KAKAO_CLIENT_SECRET", "").strip()
