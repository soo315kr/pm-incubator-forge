"""Kakao 인증 Service 구현체. 환경 변수 및 Kakao API 호출을 담당한다."""
import os
from typing import Optional
from urllib.parse import urlencode

import httpx

from kakao_authentication.schemas import (
    KakaoUserInfo,
    OAuthLinkResponse,
    TokenAndUserResponse,
)
from kakao_authentication.service_interface import KakaoAuthServiceInterface

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthServiceImpl(KakaoAuthServiceInterface):
    """Kakao OAuth 설정은 환경 변수(.env)에서 로드한다. Controller에 주입되어 인터페이스로 사용된다."""

    def __init__(self) -> None:
        self._client_id = os.environ.get("KAKAO_CLIENT_ID", "").strip()
        self._redirect_uri = os.environ.get("KAKAO_REDIRECT_URI", "").strip()
        self._client_secret = os.environ.get("KAKAO_CLIENT_SECRET", "").strip()

    def get_oauth_link(self) -> OAuthLinkResponse:
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "KAKAO_CLIENT_ID 또는 KAKAO_REDIRECT_URI가 환경 변수에 설정되지 않았습니다."
            )
        url = f"{KAKAO_AUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(url=url)

    def exchange_code_for_token_and_user(self, code: str) -> TokenAndUserResponse:
        if not code or not code.strip():
            raise ValueError("인가 코드(code)가 필요합니다.")
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "KAKAO_CLIENT_ID 또는 KAKAO_REDIRECT_URI가 환경 변수에 설정되지 않았습니다."
            )

        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "code": code.strip(),
            "client_secret": self._client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        with httpx.Client() as client:
            token_res = client.post(
                KAKAO_TOKEN_URL,
                data=payload,
                headers=headers,
            )
            token_res.raise_for_status()
            token_data = token_res.json()

        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("Kakao 토큰 응답에 access_token이 없습니다.")

        user = self._fetch_user_info(access_token)

        return TokenAndUserResponse(
            access_token=access_token,
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user,
        )

    def _fetch_user_info(self, access_token: str) -> Optional[KakaoUserInfo]:
        """액세스 토큰으로 Kakao 사용자 정보 조회 (PM-CHELSEA-4)."""
        headers = {"Authorization": f"Bearer {access_token}"}
        with httpx.Client() as client:
            res = client.get(KAKAO_USER_ME_URL, headers=headers)
            res.raise_for_status()
            data = res.json()

        kakao_id = data.get("id")
        if kakao_id is None:
            return None

        properties = data.get("kakao_account", {}) or {}
        profile = (data.get("kakao_account") or {}).get("profile") or {}
        return KakaoUserInfo(
            id=int(kakao_id),
            nickname=profile.get("nickname"),
            email=properties.get("email"),
            profile_image_url=profile.get("profile_image_url"),
        )
