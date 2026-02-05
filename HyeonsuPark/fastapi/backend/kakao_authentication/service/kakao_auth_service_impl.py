"""Kakao 인증 Service 구현체. config에서 설정을 로드한다."""

from urllib.parse import urlencode

import httpx

from kakao_authentication.config import get_client_id, get_redirect_uri
from kakao_authentication.models import (
    KakaoUserInfo,
    KakaoInvalidRequestError,
    KakaoTokenError,
    KakaoUserInfoError,
    TokenWithUserResponse,
)
from kakao_authentication.service.kakao_auth_service_interface import KakaoAuthServiceInterface

KAKAO_AUTH_HOST = "https://kauth.kakao.com"
KAKAO_API_HOST = "https://kapi.kakao.com"


class KakaoAuthServiceImpl(KakaoAuthServiceInterface):
    """Kakao OAuth 서비스 구현체."""

    def get_oauth_authorize_url(self) -> str:
        client_id = get_client_id()
        redirect_uri = get_redirect_uri()
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        return f"{KAKAO_AUTH_HOST}/oauth/authorize?{urlencode(params)}"

    def request_access_token_after_redirection(self, code: str) -> TokenWithUserResponse:
        if not code or not code.strip():
            raise KakaoInvalidRequestError("인가 코드(code)가 필요합니다.")

        client_id = get_client_id()
        redirect_uri = get_redirect_uri()

        with httpx.Client() as client:
            token_res = client.post(
                f"{KAKAO_AUTH_HOST}/oauth/token",
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
                msg = body.get("error_description", body.get("error", "토큰 발급에 실패했습니다."))
            except Exception:
                msg = token_res.text or "토큰 발급에 실패했습니다."
            raise KakaoTokenError(str(msg))

        token_data = token_res.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise KakaoTokenError("액세스 토큰을 받지 못했습니다.")

        user_info = self._get_user_info(access_token)

        return TokenWithUserResponse(
            access_token=access_token,
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _get_user_info(self, access_token: str) -> KakaoUserInfo:
        """액세스 토큰으로 Kakao 사용자 정보 조회 (PM-EDDI-4)."""
        if not access_token or not access_token.strip():
            raise KakaoUserInfoError("액세스 토큰이 필요합니다.")

        with httpx.Client() as client:
            res = client.get(
                f"{KAKAO_API_HOST}/v2/user/me",
                headers={"Authorization": f"Bearer {access_token.strip()}"},
            )

        if res.status_code == 401:
            raise KakaoUserInfoError("유효하지 않거나 만료된 액세스 토큰입니다.")
        if res.status_code != 200:
            try:
                body = res.json()
                msg = body.get("msg", body.get("error_description", "사용자 정보 조회에 실패했습니다."))
            except Exception:
                msg = res.text or "사용자 정보 조회에 실패했습니다."
            raise KakaoUserInfoError(str(msg))

        data = res.json()
        kakao_account = data.get("kakao_account", {}) or {}
        profile = kakao_account.get("profile", {}) or {}

        return KakaoUserInfo(
            id=data.get("id", 0),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
        )
