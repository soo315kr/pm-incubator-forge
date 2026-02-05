from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from .interfaces import KakaoAuthenticationService
from .schemas import (
    KakaoOAuthUrlResponse,
    KakaoTokenAndUserResponse,
)
from .service import KakaoAuthenticationServiceImpl

router = APIRouter()


def get_kakao_auth_service() -> KakaoAuthenticationService:
    """
    DI 팩토리 함수.
    Controller는 구현체 타입이 아닌 인터페이스 타입에만 의존한다.
    """
    return KakaoAuthenticationServiceImpl()


@router.get(
    "/request-oauth-link",
    response_model=KakaoOAuthUrlResponse,
    summary="Kakao OAuth 인증 URL 생성",
)
async def request_oauth_link(
    service: KakaoAuthenticationService = Depends(get_kakao_auth_service),
) -> KakaoOAuthUrlResponse:
    """
    PM-EDDI-2: Kakao 인증 URL 생성 엔드포인트.
    """
    try:
        return service.build_oauth_authorize_url()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/request-access-token-after-redirection",
    response_model=KakaoTokenAndUserResponse,
    summary="인가 코드로 Kakao 액세스 토큰 발급 및 사용자 정보 조회",
)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 리다이렉트 시 전달되는 인가 코드"),
    service: KakaoAuthenticationService = Depends(get_kakao_auth_service),
) -> KakaoTokenAndUserResponse:
    """
    PM-EDDI-3, PM-EDDI-4:
    - 인가 코드로 액세스 토큰을 발급받고
    - 해당 토큰으로 사용자 정보를 조회하여 함께 반환한다.
    """
    return await service.request_access_token_and_user_info(code=code)

