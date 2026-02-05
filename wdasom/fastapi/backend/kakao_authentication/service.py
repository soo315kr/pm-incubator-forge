from __future__ import annotations

from typing import Any, Dict
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException, status

from config.env import get_env

from .interfaces import KakaoAuthenticationService
from .schemas import (
    KakaoOAuthUrlResponse,
    KakaoTokenAndUserResponse,
    KakaoTokenResponse,
    KakaoUserProfile,
)


class KakaoAuthenticationServiceImpl(KakaoAuthenticationService):
    """
    Kakao 인증 관련 Service 구현체.

    - Kakao OAuth 인증 URL 생성 (PM-EDDI-2)
    - 인가 코드로 액세스 토큰 발급 및 사용자 정보 조회 (PM-EDDI-3, PM-EDDI-4)
    """

    KAKAO_AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def __init__(self) -> None:
        # 환경 변수 로딩은 config.env.load_env() 가 앱 시작 시점에 수행된다는 전제
        # Kakao client_id 키는 프로젝트마다 이름이 달라질 수 있어 호환되게 지원한다.
        # - KAKAO_CLIENT_ID: 사용자가 주로 쓰는 키(요청 주신 값)
        # - KAKAO_REST_API_KEY: Kakao REST API Key를 의미하는 대체 키(이전 코드)
        self.client_id = get_env("KAKAO_CLIENT_ID", None) or get_env("KAKAO_REST_API_KEY", None)
        self.redirect_uri = get_env("KAKAO_REDIRECT_URI")
        # 선택: grant_type, client_secret 등
        self.client_secret = get_env("KAKAO_CLIENT_SECRET", None)

        if not self.client_id or not self.redirect_uri:
            # 설정 자체가 누락된 경우는 서버 설정 오류로 본다.
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Kakao OAuth 환경 변수가 설정되어 있지 않습니다. "
                    "필수: KAKAO_CLIENT_ID(또는 KAKAO_REST_API_KEY), KAKAO_REDIRECT_URI"
                ),
            )

    def build_oauth_authorize_url(self) -> KakaoOAuthUrlResponse:
        """
        PM-EDDI-2: Kakao OAuth 인증 URL 생성.
        """
        query_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
        }

        url = f"{self.KAKAO_AUTH_BASE_URL}?{urlencode(query_params)}"
        return KakaoOAuthUrlResponse(url=url)

    async def request_access_token_and_user_info(
        self,
        code: str,
    ) -> KakaoTokenAndUserResponse:
        """
        PM-EDDI-3 + PM-EDDI-4:
        - 인가 코드(code)를 사용해 Kakao 토큰 서버에 액세스 토큰 요청
        - 발급받은 토큰으로 사용자 정보 조회
        """
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="인가 코드(code)가 필요합니다.",
            )

        async with httpx.AsyncClient(timeout=10.0) as client:
            token_data: Dict[str, Any] = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "code": code,
            }
            if self.client_secret:
                token_data["client_secret"] = self.client_secret

            try:
                token_resp = await client.post(self.KAKAO_TOKEN_URL, data=token_data)
            except httpx.HTTPError as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Kakao 토큰 서버 호출 실패: {exc}",
                ) from exc

            if token_resp.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Kakao 토큰 발급 실패: {token_resp.text}",
                )

            token_json = token_resp.json()
            token_model = KakaoTokenResponse(**token_json)

            # PM-EDDI-4: 발급받은 액세스 토큰으로 사용자 정보 조회
            headers = {"Authorization": f"Bearer {token_model.access_token}"}
            try:
                user_resp = await client.get(self.KAKAO_USER_INFO_URL, headers=headers)
            except httpx.HTTPError as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Kakao 사용자 정보 조회 실패: {exc}",
                ) from exc

            if user_resp.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Kakao 사용자 정보 조회 실패: {user_resp.text}",
                )

            user_json = user_resp.json()

            # Kakao 응답 구조 매핑 (필요한 필드만 사용)
            kakao_account = user_json.get("kakao_account", {}) or {}
            profile = kakao_account.get("profile", {}) or {}

            user_model = KakaoUserProfile(
                id=user_json.get("id"),
                nickname=profile.get("nickname"),
                email=kakao_account.get("email"),
            )

            return KakaoTokenAndUserResponse(token=token_model, user=user_model)

