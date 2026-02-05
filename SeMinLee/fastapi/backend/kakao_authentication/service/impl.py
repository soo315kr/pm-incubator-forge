"""
PM-EDDI-2, PM-EDDI-3, PM-EDDI-4: Kakao 인증 Service 구현체
- 환경 변수는 config(get_kakao_config)를 통해서만 사용한다.
- Kakao OAuth URL 생성, 토큰 교환, 사용자 정보 조회를 담당한다.
"""
from urllib.parse import urlencode

import httpx

from config.env import KakaoConfig, get_kakao_config
from kakao_authentication.dto.schemas import AccessTokenWithUserResponse, KakaoUserInfo
from kakao_authentication.service.interface import KakaoAuthServiceInterface

# Kakao OAuth 상수 (Kakao 공식 문서 기준)
KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"
RESPONSE_TYPE = "code"
GRANT_TYPE_AUTHORIZATION_CODE = "authorization_code"


class KakaoAuthServiceImpl(KakaoAuthServiceInterface):
    """Kakao 인증 서비스 구현체. Controller는 이 클래스에 직접 의존하지 않고 인터페이스만 사용한다."""

    def __init__(self, config: KakaoConfig) -> None:
        self._config = config

    def get_authorization_url(self) -> str:
        """PM-EDDI-2: client_id, redirect_uri, response_type 등 필수 파라미터로 Kakao OAuth URL 생성."""
        if not self._config.client_id or not self._config.redirect_uri:
            raise ValueError("KAKAO_CLIENT_ID와 KAKAO_REDIRECT_URI가 환경 변수에 설정되어야 합니다.")
        params = {
            "client_id": self._config.client_id,
            "redirect_uri": self._config.redirect_uri,
            "response_type": RESPONSE_TYPE,
        }
        return f"{KAKAO_AUTH_URL}?{urlencode(params)}"

    def request_access_token_after_redirection(self, code: str) -> AccessTokenWithUserResponse:
        """PM-EDDI-3: 인가 코드로 액세스 토큰 발급 후, PM-EDDI-4에 따라 사용자 정보를 조회하여 함께 반환."""
        if not code or not code.strip():
            raise ValueError("인가 코드(code)가 필요합니다.")
        if not self._config.client_id or not self._config.redirect_uri:
            raise ValueError("KAKAO_CLIENT_ID와 KAKAO_REDIRECT_URI가 환경 변수에 설정되어야 합니다.")

        token_payload = {
            "grant_type": GRANT_TYPE_AUTHORIZATION_CODE,
            "client_id": self._config.client_id,
            "redirect_uri": self._config.redirect_uri,
            "code": code.strip(),
        }

        with httpx.Client() as client:
            token_res = client.post(
                KAKAO_TOKEN_URL,
                data=token_payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            if token_res.status_code != 200:
                err_body = token_res.json() if token_res.headers.get("content-type", "").startswith("application/json") else {}
                msg = err_body.get("error_description", err_body.get("error", token_res.text or "토큰 발급 실패"))
                raise ValueError(str(msg))
            token_data = token_res.json()

            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("Kakao 토큰 응답에 access_token이 없습니다.")

            # PM-EDDI-4: 발급된 액세스 토큰으로 사용자 정보 조회 후 통합 반환
            user_info = self._fetch_user_info(client, access_token)

        return AccessTokenWithUserResponse(
            access_token=access_token,
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _fetch_user_info(self, client: httpx.Client, access_token: str) -> KakaoUserInfo | None:
        """PM-EDDI-4: 액세스 토큰으로 Kakao 사용자 정보(닉네임, 이메일 등) 조회."""
        try:
            res = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            res.raise_for_status()
            data = res.json()

            user_id = data.get("id")
            if user_id is not None:
                user_id = str(user_id)

            kakao_account = data.get("kakao_account") or {}
            profile = kakao_account.get("profile") or {}
            nickname = profile.get("nickname") or kakao_account.get("profile", {}).get("nickname")
            email = kakao_account.get("email")

            return KakaoUserInfo(id=user_id, nickname=nickname, email=email)
        except (httpx.HTTPStatusError, KeyError):
            return None
