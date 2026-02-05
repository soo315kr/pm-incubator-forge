"""카카오 OAuth 서비스 (인터페이스 + 구현). config.Settings만 의존."""
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from typing import Any

import httpx

from config import Settings

# 카카오 API 엔드포인트
KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_URL = "https://kapi.kakao.com/v2/user/me"

REDIRECT_PATH = "/kakao-authentication/request-access-token-after-redirection"


def _redirect_uri(settings: Settings) -> str:
    if settings.kakao_redirect_uri:
        return settings.kakao_redirect_uri
    if settings.kakao_redirect_uri_host:
        return f"{settings.kakao_redirect_uri_host.rstrip('/')}{REDIRECT_PATH}"
    return ""


class KakaoAuthService(ABC):
    """카카오 OAuth 서비스 인터페이스."""

    @abstractmethod
    def get_auth_url(self) -> str: ...

    @abstractmethod
    def get_oauth_link_response(self) -> dict[str, Any]: ...

    @abstractmethod
    async def request_access_token_after_redirection(self, code: str) -> dict[str, Any]: ...


class KakaoAuthServiceImpl(KakaoAuthService):
    """카카오 OAuth 구현. .env 기반 Settings 주입."""

    def __init__(self, settings: Settings) -> None:
        self._client_id = (settings.kakao_client_id or settings.kakao_rest_api_key) or ""
        self._redirect_uri = _redirect_uri(settings)
        self._client_secret = settings.kakao_client_secret

    def _ensure_configured(self) -> None:
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "KAKAO_CLIENT_ID(또는 KAKAO_REST_API_KEY)와 "
                "KAKAO_REDIRECT_URI_HOST(또는 KAKAO_REDIRECT_URI)를 설정해주세요."
            )

    def get_auth_url(self) -> str:
        self._ensure_configured()
        params = {"client_id": self._client_id, "redirect_uri": self._redirect_uri, "response_type": "code"}
        return f"{KAKAO_AUTH_URL}?{urlencode(params)}"

    def get_oauth_link_response(self) -> dict[str, Any]:
        return {
            "auth_url": self.get_auth_url(),
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }

    async def request_access_token_after_redirection(self, code: str) -> dict[str, Any]:
        self._ensure_configured()
        if not (code and code.strip()):
            raise ValueError("인가 코드(code)가 필요합니다.")
        code = code.strip()

        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                KAKAO_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self._client_id,
                    "redirect_uri": self._redirect_uri,
                    "code": code,
                    **({"client_secret": self._client_secret} if self._client_secret else {}),
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            token_res.raise_for_status()
            token_data = token_res.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("토큰 응답에 access_token이 없습니다.")

            user_info = await self._get_user_info(client, access_token)

        return {
            "access_token": access_token,
            "token_type": token_data.get("token_type", "bearer"),
            "refresh_token": token_data.get("refresh_token"),
            "expires_in": token_data.get("expires_in"),
            "refresh_token_expires_in": token_data.get("refresh_token_expires_in"),
            "user": user_info,
        }

    async def _get_user_info(self, client: httpx.AsyncClient, access_token: str) -> dict[str, Any]:
        res = await client.get(KAKAO_USER_URL, headers={"Authorization": f"Bearer {access_token}"})
        res.raise_for_status()
        data = res.json()
        kakao_account = data.get("kakao_account") or {}
        return {
            "id": data.get("id"),
            "kakao_account": kakao_account,
            "nickname": kakao_account.get("profile", {}).get("nickname"),
            "email": kakao_account.get("email"),
        }
