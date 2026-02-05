"""
Kakao 인증 Service 구현체.
환경 변수(.env) 기반으로 client_id, redirect_uri를 로드하며 코드에 하드코딩하지 않는다.
"""
import os
from urllib.parse import urlencode

import httpx

from kakao_authentication.exceptions import (
    InvalidAuthorizationCodeError,
    InvalidTokenError,
    KakaoApiError,
    MissingParameterError,
)
from kakao_authentication.models.schemas import (
    KakaoUserInfo,
    OAuthLinkResponse,
    TokenAndUserResponse,
)
from kakao_authentication.service.interface import KakaoAuthServiceInterface

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthServiceImpl(KakaoAuthServiceInterface):
    """Kakao 인증 Service 구현 (PM-EDDI-2, PM-EDDI-3, PM-EDDI-4)."""

    def __init__(self) -> None:
        self._client_id = os.getenv("KAKAO_CLIENT_ID")
        self._redirect_uri = os.getenv("KAKAO_REDIRECT_URI")

    def get_oauth_link(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 URL 생성 (PM-EDDI-2). 필수 파라미터 검증 후 URL 반환."""
        if not self._client_id:
            raise MissingParameterError("KAKAO_CLIENT_ID가 설정되지 않았습니다.")
        if not self._redirect_uri:
            raise MissingParameterError("KAKAO_REDIRECT_URI가 설정되지 않았습니다.")
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        auth_url = f"{KAKAO_AUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(auth_url=auth_url)

    def request_access_token_and_user(self, code: str) -> TokenAndUserResponse:
        """
        인가 코드로 토큰 발급 후 사용자 정보 조회 (PM-EDDI-3 + PM-EDDI-4).
        """
        if not code or not code.strip():
            raise MissingParameterError("인가 코드(code)가 필요합니다.")
        if not self._client_id:
            raise MissingParameterError("KAKAO_CLIENT_ID가 설정되지 않았습니다.")
        if not self._redirect_uri:
            raise MissingParameterError("KAKAO_REDIRECT_URI가 설정되지 않았습니다.")

        token_data = self._request_token(code)
        user_info = self._request_user_info(token_data["access_token"])
        return TokenAndUserResponse(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _request_token(self, code: str) -> dict:
        """Kakao 토큰 서버에 토큰 요청 (PM-EDDI-3)."""
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
            msg = body.get("error_description", body.get("error", resp.text)) or f"토큰 요청 실패 (HTTP {resp.status_code})"
            raise InvalidAuthorizationCodeError(msg, detail=resp.text)
        data = resp.json()
        return data

    def _request_user_info(self, access_token: str) -> KakaoUserInfo:
        """액세스 토큰으로 Kakao 사용자 정보 조회 (PM-EDDI-4)."""
        if not access_token or not access_token.strip():
            raise InvalidTokenError("액세스 토큰이 필요합니다.")
        with httpx.Client() as client:
            resp = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if resp.status_code == 401:
            raise InvalidTokenError("유효하지 않거나 만료된 액세스 토큰입니다.")
        if resp.status_code != 200:
            raise KakaoApiError(
                f"사용자 정보 조회 실패 (HTTP {resp.status_code})",
                status_code=resp.status_code,
                detail=resp.text,
            )
        raw = resp.json()
        user_id = raw.get("id")
        if user_id is None:
            raise KakaoApiError("사용자 정보에 id가 없습니다.", detail=resp.text)
        return KakaoUserInfo(
            id=int(user_id),
            connected_at=raw.get("connected_at"),
            properties=raw.get("properties") or {},
            kakao_account=raw.get("kakao_account") or {},
        )
