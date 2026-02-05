"""
Kakao 인증 Service 구현체.
환경 변수 기반 설정, URL/토큰/사용자 정보 로직을 담당한다.
"""

from typing import Optional
from urllib.parse import urlencode

import httpx

from config.settings import get_kakao_client_id, get_kakao_redirect_uri, get_kakao_client_secret
from kakao_authentication.schemas import (
    AccessTokenResult,
    KakaoUserInfo,
    OAuthLinkResponse,
)
from kakao_authentication.service_interface import KakaoAuthenticationServiceInterface

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthenticationServiceImpl(KakaoAuthenticationServiceInterface):
    """Kakao 인증 서비스 구현체 (PM-EDDI-2, PM-EDDI-3, PM-EDDI-4)"""

    def get_oauth_authorization_url(self) -> OAuthLinkResponse:
        client_id = get_kakao_client_id()
        redirect_uri = get_kakao_redirect_uri()
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        url = f"{KAKAO_AUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(url=url)

    def request_access_token_after_redirection(self, code: str) -> AccessTokenResult:
        client_id = get_kakao_client_id()
        redirect_uri = get_kakao_redirect_uri()
        client_secret = get_kakao_client_secret()
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        if client_secret:
            data["client_secret"] = client_secret

        with httpx.Client() as client:
            token_res = client.post(KAKAO_TOKEN_URL, data=data)
            token_res.raise_for_status()
            token_body = token_res.json()

        access_token = token_body.get("access_token")
        if not access_token:
            raise ValueError("액세스 토큰이 응답에 포함되지 않았습니다.")

        user_info = self._fetch_user_info(access_token)
        return AccessTokenResult(
            access_token=access_token,
            token_type=token_body.get("token_type", "bearer"),
            refresh_token=token_body.get("refresh_token"),
            expires_in=token_body.get("expires_in"),
            refresh_token_expires_in=token_body.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _fetch_user_info(self, access_token: str) -> Optional[KakaoUserInfo]:
        """발급된 액세스 토큰으로 Kakao 사용자 정보를 조회한다. (PM-EDDI-4)"""
        headers = {"Authorization": f"Bearer {access_token}"}
        with httpx.Client() as client:
            res = client.get(KAKAO_USER_ME_URL, headers=headers)
            if res.status_code != 200:
                return None
            body = res.json()
        if "id" not in body:
            return None
        kakao_account = body.get("kakao_account") or {}
        properties = body.get("properties") or {}
        return KakaoUserInfo(
            id=body["id"],
            nickname=properties.get("nickname"),
            email=kakao_account.get("email"),
        )
