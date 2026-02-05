"""
Kakao OAuth Service 구현체.
환경 변수(.env) 기반으로 client_id, redirect_uri 등을 로드하며 코드에 하드코딩하지 않는다.
"""
import os
from typing import Optional
from urllib.parse import urlencode

import httpx

from kakao_authentication.schemas import KakaoUserInfo, OAuthLinkResponse, TokenResponse
from kakao_authentication.service_interface import KakaoOAuthServiceInterface

# Kakao OAuth 상수 (URL만 상수, 설정값은 환경 변수)
KAKAO_AUTHORIZE_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoOAuthServiceImpl(KakaoOAuthServiceInterface):
    """Kakao OAuth Service 구현체. 환경 변수에서 client_id, redirect_uri 로드."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> None:
        self._client_id = client_id or os.getenv("KAKAO_CLIENT_ID", "")
        self._redirect_uri = redirect_uri or os.getenv("KAKAO_REDIRECT_URI", "")
        self._client_secret = client_secret or os.getenv("KAKAO_CLIENT_SECRET") or ""

    def get_oauth_authorize_url(self) -> OAuthLinkResponse:
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "필수 파라미터가 누락되었습니다. KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI 환경 변수를 확인하세요."
            )
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        oauth_url = f"{KAKAO_AUTHORIZE_URL}?{urlencode(params)}"
        return OAuthLinkResponse(oauth_url=oauth_url)

    def request_access_token_after_redirection(self, code: str) -> TokenResponse:
        if not code or not code.strip():
            raise ValueError("인가 코드(code)가 누락되었습니다.")
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "필수 파라미터가 누락되었습니다. KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI 환경 변수를 확인하세요."
            )

        data = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "code": code.strip(),
        }
        if self._client_secret:
            data["client_secret"] = self._client_secret

        with httpx.Client() as client:
            token_resp = client.post(
                KAKAO_TOKEN_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
                data=data,
            )
        token_resp.raise_for_status()
        token_body = token_resp.json()

        access_token = token_body.get("access_token")
        if not access_token:
            raise ValueError("Kakao 토큰 응답에 access_token이 없습니다.")

        user_info: Optional[KakaoUserInfo] = None
        try:
            user_info = self._fetch_user_info(access_token)
        except Exception:
            pass

        return TokenResponse(
            access_token=token_body["access_token"],
            token_type=token_body.get("token_type", "bearer"),
            expires_in=int(token_body.get("expires_in", 0)),
            refresh_token=token_body.get("refresh_token", ""),
            refresh_token_expires_in=int(token_body.get("refresh_token_expires_in", 0)),
            user=user_info,
        )

    def _fetch_user_info(self, access_token: str) -> Optional[KakaoUserInfo]:
        """액세스 토큰으로 Kakao 사용자 정보 조회 (PM-EDDI-4)."""
        with httpx.Client() as client:
            resp = client.get(
                KAKAO_USER_ME_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
        resp.raise_for_status()
        data = resp.json()

        profile = (data.get("kakao_account") or {}).get("profile") or {}
        kakao_account = data.get("kakao_account") or {}

        return KakaoUserInfo(
            id=data.get("id", 0),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
            profile_image_url=profile.get("profile_image_url"),
            thumbnail_image_url=profile.get("thumbnail_image_url"),
        )
