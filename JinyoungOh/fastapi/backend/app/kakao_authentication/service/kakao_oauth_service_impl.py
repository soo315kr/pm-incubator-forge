"""
Kakao OAuth Service 구현체.
환경 변수(.env) 기반으로 client_id, redirect_uri를 로드하고
인증 URL 생성, 인가 코드 → 액세스 토큰 교환, 액세스 토큰으로 사용자 정보 조회를 수행한다.
"""
import os
from urllib.parse import urlencode

import httpx

from app.kakao_authentication.exceptions import (
    KakaoOAuthConfigError,
    KakaoOAuthTokenError,
    KakaoUserInfoError,
)
from app.kakao_authentication.models import KakaoUserInfo, TokenResponse
from app.kakao_authentication.service.kakao_oauth_service import KakaoOAuthService

KAKAO_AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"
KAKAO_CLIENT_ID_KEY = "KAKAO_CLIENT_ID"
KAKAO_REDIRECT_URI_KEY = "KAKAO_REDIRECT_URI"
RESPONSE_TYPE = "code"
GRANT_TYPE_AUTHORIZATION_CODE = "authorization_code"


def _get_required_env(key: str) -> str:
    """환경 변수를 읽어 검증 후 반환. 없거나 비어 있으면 KakaoOAuthConfigError."""
    value = os.getenv(key)
    if not value or not value.strip():
        raise KakaoOAuthConfigError(
            f"필수 환경 변수가 없습니다: {key}. .env 파일을 확인하세요."
        )
    return value.strip()


class KakaoOAuthServiceImpl(KakaoOAuthService):
    """Kakao OAuth 서비스 구현체."""

    def get_oauth_link(self) -> str:
        """
        환경 변수에서 client_id, redirect_uri를 읽어 Kakao OAuth 인증 URL을 생성한다.
        """
        client_id = _get_required_env(KAKAO_CLIENT_ID_KEY)
        redirect_uri = _get_required_env(KAKAO_REDIRECT_URI_KEY)
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": RESPONSE_TYPE,
        }
        query = urlencode(params)
        return f"{KAKAO_AUTH_BASE_URL}?{query}"

    def exchange_code_for_token(self, code: str) -> TokenResponse:
        """
        인가 코드를 Kakao 토큰 서버에 보내 액세스 토큰을 발급받는다.
        client_id, redirect_uri는 환경 변수에서 로드한다.
        """
        if not code or not code.strip():
            raise KakaoOAuthTokenError("인가 코드(code)가 없습니다.")

        client_id = _get_required_env(KAKAO_CLIENT_ID_KEY)
        redirect_uri = _get_required_env(KAKAO_REDIRECT_URI_KEY)

        data = {
            "grant_type": GRANT_TYPE_AUTHORIZATION_CODE,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code.strip(),
        }

        with httpx.Client() as client:
            response = client.post(
                KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        if response.status_code != 200:
            try:
                body = response.json()
                error_msg = body.get("error_description") or body.get("error", "알 수 없는 오류")
            except Exception:
                error_msg = response.text or f"HTTP {response.status_code}"
            raise KakaoOAuthTokenError(
                f"토큰 발급 실패: {error_msg}"
            )

        try:
            body = response.json()
        except Exception as e:
            raise KakaoOAuthTokenError(f"토큰 응답 파싱 실패: {e}") from e

        access_token = body.get("access_token")
        refresh_token = body.get("refresh_token")
        if not access_token:
            raise KakaoOAuthTokenError("응답에 access_token이 없습니다.")

        token_response = TokenResponse(
            access_token=access_token,
            token_type=body.get("token_type", "bearer"),
            refresh_token=refresh_token or "",
            expires_in=int(body.get("expires_in", 0)),
            refresh_token_expires_in=body.get("refresh_token_expires_in"),
            scope=body.get("scope"),
        )
        # PM-EDDI-4: 발급된 액세스 토큰으로 사용자 정보 조회 후 함께 반환
        try:
            token_response.user_info = self.get_user_info(access_token)
        except KakaoUserInfoError:
            # 사용자 정보 조회 실패 시 토큰만 반환 (user_info는 None)
            pass
        return token_response

    def get_user_info(self, access_token: str) -> KakaoUserInfo:
        """
        액세스 토큰으로 Kakao /v2/user/me를 호출해 사용자 정보를 조회한다.
        토큰이 유효하지 않거나 만료된 경우 KakaoUserInfoError를 발생시킨다.
        """
        if not access_token or not access_token.strip():
            raise KakaoUserInfoError("액세스 토큰이 없습니다.")

        with httpx.Client() as client:
            response = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token.strip()}"},
            )

        if response.status_code == 401:
            raise KakaoUserInfoError(
                "액세스 토큰이 유효하지 않거나 만료되었습니다. 다시 로그인해 주세요."
            )
        if response.status_code != 200:
            try:
                body = response.json()
                error_msg = body.get("msg") or body.get("error_description") or body.get("error", "알 수 없는 오류")
            except Exception:
                error_msg = response.text or f"HTTP {response.status_code}"
            raise KakaoUserInfoError(f"사용자 정보 조회 실패: {error_msg}")

        try:
            body = response.json()
        except Exception as e:
            raise KakaoUserInfoError(f"응답 파싱 실패: {e}") from e

        user_id = body.get("id")
        if user_id is None:
            raise KakaoUserInfoError("응답에 사용자 ID가 없습니다.")

        # kakao_account (권장) 또는 properties (레거시)에서 프로필 추출
        kakao_account = body.get("kakao_account") or {}
        profile = kakao_account.get("profile") or {}
        properties = body.get("properties") or {}

        nickname = (
            profile.get("nickname")
            or properties.get("nickname")
        )
        profile_image_url = (
            profile.get("profile_image_url")
            or properties.get("profile_image")
        )
        thumbnail_image_url = (
            profile.get("thumbnail_image_url")
            or properties.get("thumbnail_image")
        )
        email = kakao_account.get("email")

        return KakaoUserInfo(
            id=int(user_id),
            nickname=nickname,
            email=email,
            profile_image_url=profile_image_url,
            thumbnail_image_url=thumbnail_image_url,
        )
