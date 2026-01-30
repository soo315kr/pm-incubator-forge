from urllib.parse import urlencode
import httpx
from fastapi import HTTPException

from config.env import get_kakao_client_id, get_kakao_redirect_uri
from kakao_authentication.service.kakao_oauth_service_interface import KakaoOAuthServiceInterface
from kakao_authentication.schemas.kakao_oauth import (
    KakaoAuthUrlResponse,
    KakaoTokenResponse,
    KakaoUserInfoResponse,
)


class KakaoOAuthServiceImpl(KakaoOAuthServiceInterface):
    """Kakao OAuth Service 구현체"""

    KAKAO_AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def __init__(self):
        self._client_id = get_kakao_client_id()
        self._redirect_uri = get_kakao_redirect_uri()

    def generate_auth_url(self) -> KakaoAuthUrlResponse:
        """
        Kakao 인증 URL 생성

        Returns:
            KakaoAuthUrlResponse: 인증 URL 및 관련 정보

        Raises:
            HTTPException: 필수 환경 변수가 설정되지 않은 경우
        """
        if not self._client_id:
            raise HTTPException(
                status_code=500,
                detail="KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다."
            )

        if not self._redirect_uri:
            raise HTTPException(
                status_code=500,
                detail="KAKAO_REDIRECT_URI 환경 변수가 설정되지 않았습니다."
            )

        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }

        auth_url = f"{self.KAKAO_AUTH_BASE_URL}?{urlencode(params)}"

        return KakaoAuthUrlResponse(
            auth_url=auth_url,
            client_id=self._client_id,
            redirect_uri=self._redirect_uri,
            response_type="code",
        )

    async def request_access_token(self, code: str) -> KakaoTokenResponse:
        """
        인가 코드로 액세스 토큰 요청

        Args:
            code: Kakao 인증 후 발급된 인가 코드

        Returns:
            KakaoTokenResponse: 액세스 토큰 및 관련 정보

        Raises:
            HTTPException: 토큰 요청 실패 시
        """
        if not self._client_id:
            raise HTTPException(
                status_code=500,
                detail="KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다."
            )

        if not self._redirect_uri:
            raise HTTPException(
                status_code=500,
                detail="KAKAO_REDIRECT_URI 환경 변수가 설정되지 않았습니다."
            )

        if not code:
            raise HTTPException(
                status_code=400,
                detail="인가 코드(code)가 제공되지 않았습니다."
            )

        data = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "code": code,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code != 200:
                error_data = response.json()
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"토큰 요청 실패: {error_data.get('error_description', error_data.get('error', '알 수 없는 오류'))}"
                )

            token_data = response.json()

        return KakaoTokenResponse(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data["expires_in"],
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            scope=token_data.get("scope"),
        )

    async def get_user_info(self, access_token: str) -> KakaoUserInfoResponse:
        """
        액세스 토큰으로 사용자 정보 조회

        Args:
            access_token: 유효한 Kakao 액세스 토큰

        Returns:
            KakaoUserInfoResponse: 사용자 정보

        Raises:
            HTTPException: 사용자 정보 조회 실패 시
        """
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail="액세스 토큰이 제공되지 않았습니다."
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.KAKAO_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code != 200:
                if response.status_code == 401:
                    raise HTTPException(
                        status_code=401,
                        detail="액세스 토큰이 유효하지 않거나 만료되었습니다."
                    )
                raise HTTPException(
                    status_code=response.status_code,
                    detail="사용자 정보 조회에 실패했습니다."
                )

            user_data = response.json()

        kakao_account = user_data.get("kakao_account", {})
        profile = kakao_account.get("profile", {})

        return KakaoUserInfoResponse(
            id=user_data["id"],
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
            profile_image_url=profile.get("profile_image_url"),
        )
