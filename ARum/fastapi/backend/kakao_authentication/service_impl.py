"""Kakao 인증 Service 구현체. 환경 변수 기반 설정, Kakao API 호출."""

import os
from urllib.parse import urlencode

import httpx

from kakao_authentication.exceptions import (
    InvalidRequestError,
    KakaoApiError,
    MissingConfigError,
)
from kakao_authentication.schemas import (
    KakaoUserInfo,
    OAuthLinkResponse,
    TokenWithUserResponse,
)
from kakao_authentication.service_interface import KakaoAuthenticationServiceInterface

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthenticationServiceImpl(KakaoAuthenticationServiceInterface):
    """Kakao OAuth Service 구현. client_id, redirect_uri는 환경 변수에서 로드한다."""

    def _get_client_id(self) -> str:
        value = os.getenv("KAKAO_CLIENT_ID")
        if not value or not value.strip():
            raise MissingConfigError("KAKAO_CLIENT_ID가 설정되지 않았습니다.")
        return value.strip()

    def _get_redirect_uri(self) -> str:
        value = os.getenv("KAKAO_REDIRECT_URI")
        if not value or not value.strip():
            raise MissingConfigError("KAKAO_REDIRECT_URI가 설정되지 않았습니다.")
        return value.strip()

    def get_oauth_link(self) -> OAuthLinkResponse:
        client_id = self._get_client_id()
        redirect_uri = self._get_redirect_uri()
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        oauth_link = f"{KAKAO_AUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(oauth_link=oauth_link)

    def request_access_token_after_redirection(self, code: str) -> TokenWithUserResponse:
        if not code or not code.strip():
            raise InvalidRequestError("인가 코드(code)가 필요합니다.")

        client_id = self._get_client_id()
        redirect_uri = self._get_redirect_uri()

        with httpx.Client() as client:
            token_res = client.post(
                KAKAO_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                    "code": code.strip(),
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        if token_res.status_code != 200:
            try:
                body = token_res.json()
                msg = body.get("error_description", body.get("error", "토큰 발급 실패"))
            except Exception:
                msg = "Kakao 토큰 발급에 실패했습니다."
            raise KakaoApiError(str(msg), status_code=502)

        data = token_res.json()
        access_token = data.get("access_token")
        if not access_token:
            raise KakaoApiError("액세스 토큰을 받지 못했습니다.", status_code=502)

        user_info = self._fetch_user_info(access_token)

        return TokenWithUserResponse(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "bearer"),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in"),
            refresh_token_expires_in=data.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _fetch_user_info(self, access_token: str) -> KakaoUserInfo:
        """액세스 토큰으로 Kakao 사용자 정보 조회 (PM-EDDI-4)."""
        with httpx.Client() as client:
            res = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )

        if res.status_code != 200:
            try:
                body = res.json()
                msg = body.get("msg", "사용자 정보 조회 실패")
            except Exception:
                msg = "Kakao 사용자 정보 조회에 실패했습니다."
            raise KakaoApiError(str(msg), status_code=502)

        data = res.json()
        kakao_id = data.get("id")
        if kakao_id is None:
            raise KakaoApiError("사용자 ID를 조회할 수 없습니다.", status_code=502)

        properties = data.get("properties") or {}
        kakao_account = data.get("kakao_account") or {}
        email = None
        if isinstance(kakao_account.get("email"), str):
            email = kakao_account["email"]

        return KakaoUserInfo(
            id=int(kakao_id),
            nickname=properties.get("nickname"),
            email=email,
        )
