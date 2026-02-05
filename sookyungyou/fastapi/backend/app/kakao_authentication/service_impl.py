"""Kakao 인증 Service 구현체. 환경 변수 및 Kakao API 호출을 담당한다."""

import os
from urllib.parse import urlencode

import httpx

from app.kakao_authentication.exceptions import (
    InvalidAccessTokenError,
    InvalidAuthorizationCodeError,
    InvalidOAuthConfigError,
    KakaoApiError,
)
from app.kakao_authentication.schemas import (
    KakaoUserInfo,
    OAuthLinkResponse,
    TokenWithUserResponse,
)
from app.kakao_authentication.service_interface import KakaoAuthenticationServiceInterface

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoAuthenticationServiceImpl(KakaoAuthenticationServiceInterface):
    """Kakao 인증 서비스 구현체. 환경 변수(.env)에서 client_id, redirect_uri를 로드한다."""

    def _get_client_id(self) -> str:
        value = os.getenv("KAKAO_CLIENT_ID", "").strip()
        if not value:
            raise InvalidOAuthConfigError("KAKAO_CLIENT_ID가 설정되지 않았습니다.")
        return value

    def _get_redirect_uri(self) -> str:
        value = os.getenv("KAKAO_REDIRECT_URI", "").strip()
        if not value:
            raise InvalidOAuthConfigError("KAKAO_REDIRECT_URI가 설정되지 않았습니다.")
        return value

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

    def _request_access_token(self, code: str) -> dict:
        client_id = self._get_client_id()
        redirect_uri = self._get_redirect_uri()
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        with httpx.Client() as client:
            resp = client.post(
                KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        if resp.status_code != 200:
            try:
                err = resp.json()
                msg = err.get("error_description", err.get("error", resp.text))
            except Exception:
                msg = resp.text or "토큰 발급에 실패했습니다."
            raise InvalidAuthorizationCodeError(str(msg))
        return resp.json()

    def _request_user_info(self, access_token: str) -> KakaoUserInfo:
        with httpx.Client() as client:
            resp = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if resp.status_code == 401:
            raise InvalidAccessTokenError("액세스 토큰이 유효하지 않거나 만료되었습니다.")
        if resp.status_code != 200:
            raise KakaoApiError("사용자 정보 조회에 실패했습니다.", status_code=resp.status_code)
        try:
            data = resp.json()
        except Exception as e:
            raise KakaoApiError(f"응답 파싱 실패: {e}")

        kakao_id = data.get("id")
        if kakao_id is None:
            raise KakaoApiError("사용자 ID가 없습니다.")

        kakao_account = data.get("kakao_account") or {}
        profile = kakao_account.get("profile") or {}
        return KakaoUserInfo(
            id=int(kakao_id),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
        )

    def exchange_code_for_token_with_user(self, code: str) -> TokenWithUserResponse:
        if not (code and code.strip()):
            raise InvalidAuthorizationCodeError("인가 코드(code)가 필요합니다.")
        code = code.strip()

        token_data = self._request_access_token(code)
        access_token = token_data.get("access_token")
        if not access_token:
            raise InvalidAuthorizationCodeError("액세스 토큰을 받지 못했습니다.")

        user = self._request_user_info(access_token)

        return TokenWithUserResponse(
            access_token=access_token,
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user,
        )
