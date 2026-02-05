"""Kakao 인증 Service 구현체. 환경 변수 및 Kakao API 호출을 담당한다."""

import os
from urllib.parse import urlencode

import httpx

from kakao_authentication.schemas import (
    KakaoUserInfo,
    OAuthLinkResponse,
    TokenAndUserResponse,
)

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthServiceImpl:
    """Kakao OAuth Service 구현체. client_id, redirect_uri는 환경 변수에서 로드한다."""

    def __init__(self) -> None:
        self._client_id = os.getenv("KAKAO_CLIENT_ID", "").strip()
        self._redirect_uri = os.getenv("KAKAO_REDIRECT_URI", "").strip()

    def get_oauth_link(self) -> OAuthLinkResponse:
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI가 환경 변수에 설정되어 있지 않습니다."
            )
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        url = f"{KAKAO_AUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(url=url)

    def exchange_code_for_token_and_user(self, code: str) -> TokenAndUserResponse:
        if not code or not code.strip():
            raise ValueError("인가 코드(code)가 필요합니다.")
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI가 환경 변수에 설정되어 있지 않습니다."
            )

        token_data = self._request_access_token(code.strip())
        user_info = self._request_user_info(token_data["access_token"])
        return TokenAndUserResponse(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=int(token_data.get("expires_in", 0)),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _request_access_token(self, code: str) -> dict:
        """Kakao 토큰 서버에 인가 코드로 액세스 토큰 요청."""
        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "code": code,
        }
        with httpx.Client() as client:
            resp = client.post(
                KAKAO_TOKEN_URL,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        if resp.status_code != 200:
            body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            msg = body.get("error_description", body.get("error", resp.text)) or "토큰 발급에 실패했습니다."
            raise ValueError(msg)
        return resp.json()

    def _request_user_info(self, access_token: str) -> KakaoUserInfo:
        """액세스 토큰으로 Kakao 사용자 정보 조회."""
        if not access_token or not access_token.strip():
            raise ValueError("유효한 액세스 토큰이 필요합니다.")
        with httpx.Client() as client:
            resp = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token.strip()}"},
            )
        if resp.status_code == 401:
            raise ValueError("액세스 토큰이 유효하지 않거나 만료되었습니다.")
        if resp.status_code != 200:
            raise ValueError("사용자 정보 조회에 실패했습니다.")
        data = resp.json()
        kakao_account = data.get("kakao_account", {}) or {}
        profile = kakao_account.get("profile", {}) or {}
        return KakaoUserInfo(
            id=data.get("id", 0),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
        )
