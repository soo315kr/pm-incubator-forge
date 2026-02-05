"""
Kakao OAuth 인증 URL 생성, 토큰 교환 및 사용자 정보 조회 Service 구현체.
환경 변수 기반 설정을 사용하며, URL 구성·토큰 요청·사용자 정보 조회 로직만 담당한다.
"""

from urllib.parse import urlencode

import httpx

from config.kakao import (
    get_kakao_client_id,
    get_kakao_client_secret,
    get_kakao_redirect_uri,
)

from kakao_authentication.dto import TokenResponse, TokenWithUserResponse, UserInfo
from kakao_authentication.exceptions import (
    KakaoOAuthConfigError,
    KakaoTokenError,
    KakaoUserInfoError,
)
from kakao_authentication.service_interface import KakaoAuthServiceInterface

KAKAO_AUTHORIZE_BASE = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"
RESPONSE_TYPE = "code"
GRANT_TYPE_AUTHORIZATION_CODE = "authorization_code"


def _require_client_id() -> str:
    client_id = get_kakao_client_id()
    if not client_id or not client_id.strip():
        raise KakaoOAuthConfigError(
            "Kakao OAuth 설정이 누락되었습니다: KAKAO_CLIENT_ID를 .env에 설정해 주세요."
        )
    return client_id.strip()


def _require_redirect_uri() -> str:
    redirect_uri = get_kakao_redirect_uri()
    if not redirect_uri or not redirect_uri.strip():
        raise KakaoOAuthConfigError(
            "Kakao OAuth 설정이 누락되었습니다: KAKAO_REDIRECT_URI를 .env에 설정해 주세요."
        )
    return redirect_uri.strip()


class KakaoAuthService(KakaoAuthServiceInterface):
    """Kakao OAuth 인증 URL 생성 및 토큰 교환 서비스 구현체."""

    def get_authorization_url(self) -> str:
        client_id = _require_client_id()
        redirect_uri = _require_redirect_uri()
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": RESPONSE_TYPE,
        }
        return f"{KAKAO_AUTHORIZE_BASE}?{urlencode(params)}"

    def _fetch_user_info(self, access_token: str) -> UserInfo:
        """액세스 토큰으로 Kakao 사용자 정보를 조회한다. 유효하지 않거나 만료 시 KakaoUserInfoError."""
        try:
            resp = httpx.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0,
            )
        except httpx.RequestError as e:
            raise KakaoUserInfoError(f"Kakao 사용자 정보 요청 중 오류가 발생했습니다: {e!s}")

        if resp.status_code == 401:
            raise KakaoUserInfoError(
                "액세스 토큰이 유효하지 않거나 만료되었습니다. 다시 로그인해 주세요."
            )
        if resp.status_code != 200:
            try:
                err_body = resp.json()
                err_msg = err_body.get("msg") or err_body.get("error_description") or resp.text
            except Exception:
                err_msg = resp.text or f"HTTP {resp.status_code}"
            raise KakaoUserInfoError(f"사용자 정보 조회 실패: {err_msg}")

        try:
            body = resp.json()
            user_id = int(body["id"])
        except (KeyError, TypeError, ValueError) as e:
            raise KakaoUserInfoError(f"Kakao 사용자 정보 응답 형식이 올바르지 않습니다: {e!s}")

        kakao_account = body.get("kakao_account") or {}
        profile = kakao_account.get("profile") or {}
        nickname = (
            profile.get("nickname")
            or (body.get("properties") or {}).get("nickname")
        )
        email = kakao_account.get("email")
        profile_image_url = profile.get("profile_image_url")
        thumbnail_image_url = profile.get("thumbnail_image_url")

        return UserInfo(
            id=user_id,
            nickname=nickname,
            email=email,
            profile_image_url=profile_image_url,
            thumbnail_image_url=thumbnail_image_url,
        )

    def exchange_code_for_tokens(self, code: str) -> TokenWithUserResponse:
        if not code or not code.strip():
            raise KakaoTokenError("인가 코드(code)가 누락되었습니다.")

        client_id = _require_client_id()
        redirect_uri = _require_redirect_uri()
        client_secret = get_kakao_client_secret()
        if client_secret:
            client_secret = client_secret.strip()

        data = {
            "grant_type": GRANT_TYPE_AUTHORIZATION_CODE,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code.strip(),
        }
        if client_secret:
            data["client_secret"] = client_secret

        try:
            resp = httpx.post(
                KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10.0,
            )
        except httpx.RequestError as e:
            raise KakaoTokenError(f"Kakao 토큰 서버 요청 중 오류가 발생했습니다: {e!s}")

        if resp.status_code != 200:
            try:
                err_body = resp.json()
                err_msg = err_body.get("error_description") or err_body.get("error") or resp.text
            except Exception:
                err_msg = resp.text or f"HTTP {resp.status_code}"
            raise KakaoTokenError(f"토큰 발급 실패: {err_msg}")

        try:
            body = resp.json()
            token_response = TokenResponse(
                access_token=body["access_token"],
                token_type=body.get("token_type", "bearer"),
                refresh_token=body["refresh_token"],
                expires_in=int(body["expires_in"]),
                refresh_token_expires_in=int(body["refresh_token_expires_in"]),
                scope=body.get("scope"),
            )
        except (KeyError, TypeError, ValueError) as e:
            raise KakaoTokenError(f"Kakao 토큰 응답 형식이 올바르지 않습니다: {e!s}")

        user_info = self._fetch_user_info(token_response.access_token)

        return TokenWithUserResponse(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            refresh_token=token_response.refresh_token,
            expires_in=token_response.expires_in,
            refresh_token_expires_in=token_response.refresh_token_expires_in,
            scope=token_response.scope,
            user=user_info,
        )
