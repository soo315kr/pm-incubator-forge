from fastapi import APIRouter, Depends, Query

from kakao_authentication.service import KakaoOAuthServiceInterface, KakaoOAuthServiceImpl
from kakao_authentication.schemas.kakao_oauth import (
    KakaoAuthUrlResponse,
    KakaoAuthCompleteResponse,
)

router = APIRouter(prefix="/kakao-authentication", tags=["Kakao Authentication"])


def get_kakao_oauth_service() -> KakaoOAuthServiceInterface:
    """Kakao OAuth Service 의존성 주입"""
    return KakaoOAuthServiceImpl()


@router.get("/request-oauth-link", response_model=KakaoAuthUrlResponse)
async def request_oauth_link(
    service: KakaoOAuthServiceInterface = Depends(get_kakao_oauth_service),
):
    """
    Kakao OAuth 인증 URL 생성

    사용자가 Kakao 인증을 요청할 때 인증 URL을 생성하여 반환합니다.

    Returns:
        KakaoAuthUrlResponse: 인증 URL 및 관련 정보
    """
    return service.generate_auth_url()


@router.get("/request-access-token-after-redirection", response_model=KakaoAuthCompleteResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 발급된 인가 코드"),
    service: KakaoOAuthServiceInterface = Depends(get_kakao_oauth_service),
):
    """
    인가 코드로 액세스 토큰 요청 및 사용자 정보 조회

    Kakao 인증 후 리다이렉트로 받은 인가 코드를 사용하여
    액세스 토큰을 발급받고 사용자 정보를 조회하여 반환합니다.

    Args:
        code: Kakao 인증 후 발급된 인가 코드

    Returns:
        KakaoAuthCompleteResponse: 토큰 정보 및 사용자 정보
    """
    token_response = await service.request_access_token(code)
    user_info_response = await service.get_user_info(token_response.access_token)

    return KakaoAuthCompleteResponse(
        token=token_response,
        user_info=user_info_response,
    )
