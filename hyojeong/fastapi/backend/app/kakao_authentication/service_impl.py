from __future__ import annotations

from typing import Final

import httpx

from app.config.env import get_env

from .schemas import KakaoUserInfo, TokenResponse
from .service import KakaoAuthenticationService

_DEFAULT_AUTH_URL: Final[str] = "https://kauth.kakao.com/oauth/authorize"
_DEFAULT_TOKEN_URL: Final[str] = "https://kauth.kakao.com/oauth/token"
_DEFAULT_USER_INFO_URL: Final[str] = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthenticationServiceImpl(KakaoAuthenticationService):
    def __init__(self) -> None:
        self._client_id = get_env("KAKAO_CLIENT_ID")
        self._redirect_uri = get_env("KAKAO_REDIRECT_URI")
        self._auth_url = get_env("KAKAO_AUTH_URL", _DEFAULT_AUTH_URL)
        self._token_url = get_env("KAKAO_TOKEN_URL", _DEFAULT_TOKEN_URL)
        self._user_info_url = get_env("KAKAO_USER_INFO_URL", _DEFAULT_USER_INFO_URL)

    def _require(self, value: str | None, name: str) -> str:
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value

    def build_oauth_link(self) -> str:
        client_id = self._require(self._client_id, "KAKAO_CLIENT_ID")
        redirect_uri = self._require(self._redirect_uri, "KAKAO_REDIRECT_URI")

        response_type = "code"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
        }

        return str(httpx.URL(self._auth_url, params=params))

    async def request_access_token(self, code: str) -> TokenResponse:
        if not code:
            raise ValueError("Missing required query parameter: code")

        client_id = self._require(self._client_id, "KAKAO_CLIENT_ID")
        redirect_uri = self._require(self._redirect_uri, "KAKAO_REDIRECT_URI")

        payload = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(self._token_url, data=payload)
        if response.status_code >= 400:
            raise RuntimeError(f"Kakao token request failed: {response.text}")

        data = response.json()
        access_token = data.get("access_token")
        if not access_token:
            raise RuntimeError("Kakao token response missing access_token")

        return TokenResponse(
            access_token=access_token,
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type"),
            expires_in=data.get("expires_in"),
            scope=data.get("scope"),
        )

    async def fetch_user_info(self, access_token: str) -> KakaoUserInfo:
        if not access_token:
            raise ValueError("Missing access token")

        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self._user_info_url, headers=headers)
        if response.status_code >= 400:
            raise RuntimeError(f"Kakao user info request failed: {response.text}")

        data = response.json()
        account = data.get("kakao_account") or {}
        profile = account.get("profile") or {}

        user_id = data.get("id")
        if user_id is None:
            raise RuntimeError("Kakao user info response missing id")

        return KakaoUserInfo(
            id=user_id,
            nickname=profile.get("nickname"),
            email=account.get("email"),
        )
