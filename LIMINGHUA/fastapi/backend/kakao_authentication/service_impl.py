import os
from urllib.parse import urlencode

import httpx

from kakao_authentication.schemas import (
    KakaoUserInfo,
    OAuthLinkResponse,
    TokenWithUserResponse,
)
from kakao_authentication.service_interface import KakaoAuthServiceInterface

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


def _get_client_id() -> str:
    value = os.getenv("KAKAO_CLIENT_ID")
    if not value:
        raise ValueError("KAKAO_CLIENT_ID is not set in environment")
    return value


def _get_redirect_uri() -> str:
    value = os.getenv("KAKAO_REDIRECT_URI")
    if not value:
        raise ValueError("KAKAO_REDIRECT_URI is not set in environment")
    return value


def _build_oauth_url(client_id: str, redirect_uri: str) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
    }
    return f"{KAKAO_AUTH_URL}?{urlencode(params)}"


class KakaoAuthServiceImpl(KakaoAuthServiceInterface):
    """Implementation of Kakao OAuth; uses env for client_id and redirect_uri."""

    def get_oauth_link(self) -> OAuthLinkResponse:
        client_id = _get_client_id()
        redirect_uri = _get_redirect_uri()
        url = _build_oauth_url(client_id, redirect_uri)
        return OAuthLinkResponse(url=url)

    def exchange_code_for_token_and_user(self, code: str) -> TokenWithUserResponse:
        if not code or not code.strip():
            raise ValueError("Authorization code is required")
        client_id = _get_client_id()
        redirect_uri = _get_redirect_uri()
        with httpx.Client() as http_client:
            token_res = http_client.post(
                KAKAO_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                    "code": code.strip(),
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            token_res.raise_for_status()
            token_data = token_res.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("Kakao did not return an access_token")
        user_info = _fetch_user_info(access_token)
        return TokenWithUserResponse(
            access_token=access_token,
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            scope=token_data.get("scope"),
            user=user_info,
        )


def _fetch_user_info(access_token: str) -> KakaoUserInfo | None:
    with httpx.Client() as http_client:
        res = http_client.get(
            KAKAO_USER_ME_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if res.status_code == 401:
            raise ValueError("Access token is invalid or expired")
        if res.status_code != 200:
            return None
        data = res.json()
    kakao_account = data.get("kakao_account") or {}
    properties = data.get("properties") or {}
    return KakaoUserInfo(
        id=data.get("id", 0),
        nickname=properties.get("nickname"),
        email=kakao_account.get("email"),
        profile_image_url=properties.get("profile_image"),
    )
