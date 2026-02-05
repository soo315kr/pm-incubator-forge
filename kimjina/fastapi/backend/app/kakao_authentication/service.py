"""Kakao 인증 Service Interface 및 구현체 (Layered Architecture)."""

from typing import Protocol

from app.kakao_authentication.schemas import KakaoUserInfo, TokenWithUserInfoResponse


class KakaoAuthenticationService(Protocol):
    """PM-EDDI-2/3: Controller가 의존하는 Service Interface. 구현체에 직접 의존하지 않는다."""

    def get_oauth_authorize_url(self) -> str:
        """Kakao OAuth 인증 URL을 생성하여 반환한다."""
        ...

    def request_access_token_after_redirection(self, code: str) -> TokenWithUserInfoResponse:
        """인가 코드로 액세스 토큰을 요청하고, 발급된 토큰으로 사용자 정보를 조회하여 반환한다."""
        ...


class KakaoAuthenticationServiceImpl:
    """Kakao 인증 Service 구현체. 환경 변수(.env) 기반 설정을 사용한다."""

    def __init__(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        client_secret: str,
        authorize_url: str,
        token_url: str,
        user_info_url: str,
    ):
        self._client_id = client_id
        self._redirect_uri = redirect_uri
        self._client_secret = client_secret
        self._authorize_url = authorize_url
        self._token_url = token_url
        self._user_info_url = user_info_url

    def get_oauth_authorize_url(self) -> str:
        from urllib.parse import urlencode

        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "Kakao OAuth 설정이 누락되었습니다. (client_id, redirect_uri)"
            )
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        return f"{self._authorize_url}?{urlencode(params)}"

    def request_access_token_after_redirection(self, code: str) -> TokenWithUserInfoResponse:
        import httpx

        if not code or not code.strip():
            raise ValueError("인가 코드(code)가 필요합니다.")
        if not self._client_id or not self._redirect_uri:
            raise ValueError(
                "Kakao OAuth 설정이 누락되었습니다. (client_id, redirect_uri)"
            )

        with httpx.Client() as client:
            token_res = client.post(
                self._token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self._client_id,
                    "redirect_uri": self._redirect_uri,
                    "code": code.strip(),
                    **(
                        {"client_secret": self._client_secret}
                        if self._client_secret
                        else {}
                    ),
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            if token_res.status_code != 200:
                try:
                    err = token_res.json()
                    detail = err.get("error_description", err.get("error", token_res.text))
                except Exception:
                    detail = token_res.text
                raise ValueError(f"Kakao 토큰 발급 실패: {detail}")

            token_data = token_res.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("Kakao 응답에 access_token이 없습니다.")

            user_info = self._fetch_user_info(client, access_token)

        return TokenWithUserInfoResponse(
            access_token=access_token,
            token_type=token_data.get("token_type", "bearer"),
            expires_in=token_data.get("expires_in"),
            refresh_token=token_data.get("refresh_token"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            user=user_info,
        )

    def _fetch_user_info(self, client: "httpx.Client", access_token: str) -> KakaoUserInfo:
        """PM-EDDI-4: 액세스 토큰으로 Kakao 사용자 정보 조회."""
        user_res = client.get(
            self._user_info_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if user_res.status_code != 200:
            try:
                err = user_res.json()
                detail = err.get("msg", err.get("error_description", user_res.text))
            except Exception:
                detail = user_res.text
            raise ValueError(f"Kakao 사용자 정보 조회 실패: {detail}")

        data = user_res.json()
        kakao_account = data.get("kakao_account", {})
        profile = kakao_account.get("profile", {})

        return KakaoUserInfo(
            id=data.get("id", 0),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
            profile_image_url=profile.get("profile_image_url"),
        )
