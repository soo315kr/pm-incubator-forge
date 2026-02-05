"""
Kakao 인증 서비스 구현체
"""
import urllib.parse
import httpx
from config.env import get_env
from models.kakao_authentication import (
    OAuthLinkResponse,
    AccessTokenResponse,
    KakaoUserInfo,
)
from services.interfaces.kakao_authentication import KakaoAuthenticationServiceInterface


class KakaoAuthenticationServiceImpl(KakaoAuthenticationServiceInterface):
    """Kakao 인증 서비스 구현체"""

    KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def __init__(self):
        self._client_id = None
        self._redirect_uri = None
        self._client_secret = None

    def _get_client_id(self) -> str:
        if self._client_id is None:
            self._client_id = get_env("KAKAO_CLIENT_ID")
        return self._client_id

    def _get_redirect_uri(self) -> str:
        if self._redirect_uri is None:
            self._redirect_uri = get_env("KAKAO_REDIRECT_URI")
        return self._redirect_uri

    def _get_client_secret(self) -> str:
        if self._client_secret is None:
            try:
                self._client_secret = get_env("KAKAO_CLIENT_SECRET")
            except ValueError:
                self._client_secret = ""
        return self._client_secret

    def generate_oauth_link(self) -> OAuthLinkResponse:
        client_id = self._get_client_id()
        redirect_uri = self._get_redirect_uri()
        if not client_id or not redirect_uri:
            raise ValueError("KAKAO_CLIENT_ID 또는 KAKAO_REDIRECT_URI가 설정되지 않았습니다.")
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        auth_url = f"{self.KAKAO_AUTH_URL}?{urllib.parse.urlencode(params)}"
        return OAuthLinkResponse(auth_url=auth_url)

    def request_access_token(self, code: str) -> AccessTokenResponse:
        if not code:
            raise ValueError("인가 코드(code)가 필요합니다.")
        client_id = self._get_client_id()
        redirect_uri = self._get_redirect_uri()
        client_secret = self._get_client_secret()
        if not client_id or not redirect_uri:
            raise ValueError("KAKAO_CLIENT_ID 또는 KAKAO_REDIRECT_URI가 설정되지 않았습니다.")
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        if client_secret:
            data["client_secret"] = client_secret
        try:
            response = httpx.post(
                self.KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            token_data = response.json()
            return AccessTokenResponse(
                access_token=token_data.get("access_token"),
                token_type=token_data.get("token_type", "bearer"),
                refresh_token=token_data.get("refresh_token"),
                expires_in=token_data.get("expires_in"),
                refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
                scope=token_data.get("scope"),
            )
        except httpx.HTTPStatusError as e:
            error_msg = f"Kakao 토큰 요청 실패: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error_description", error_msg)
            except Exception:
                pass
            raise Exception(error_msg) from e
        except Exception as e:
            raise Exception(f"액세스 토큰 요청 중 오류 발생: {str(e)}") from e

    def get_user_info(self, access_token: str) -> KakaoUserInfo:
        if not access_token:
            raise ValueError("액세스 토큰이 필요합니다.")
        try:
            response = httpx.get(
                self.KAKAO_USER_INFO_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            response.raise_for_status()
            user_data = response.json()
            kakao_account = user_data.get("kakao_account", {})
            properties = user_data.get("properties", {})
            return KakaoUserInfo(
                id=user_data.get("id"),
                nickname=properties.get("nickname"),
                email=kakao_account.get("email"),
                profile_image=properties.get("profile_image"),
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("유효하지 않은 액세스 토큰입니다.") from e
            error_msg = f"Kakao 사용자 정보 조회 실패: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error_description", error_msg)
            except Exception:
                pass
            raise Exception(error_msg) from e
        except Exception as e:
            raise Exception(f"사용자 정보 조회 중 오류 발생: {str(e)}") from e
