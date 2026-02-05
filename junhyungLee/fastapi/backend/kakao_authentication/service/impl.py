"""Kakao 인증 Service 구현체 (PM-EDDI-2). 환경 변수 기반 client_id, redirect_uri."""

import os
from urllib.parse import urlencode

KAKAO_AUTH_BASE = "https://kauth.kakao.com/oauth/authorize"


def _get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or not value.strip():
        raise ValueError(f"필수 환경 변수가 없거나 비어 있습니다: {name}")
    return value.strip()


class KakaoAuthServiceImpl:
    """Kakao OAuth 인증 URL 생성 구현체. .env에서 client_id, redirect_uri 로드."""

    def get_oauth_authorization_url(self) -> str:
        client_id = _get_required_env("KAKAO_CLIENT_ID")
        redirect_uri = _get_required_env("KAKAO_REDIRECT_URI")
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        return f"{KAKAO_AUTH_BASE}?{urlencode(params)}"
