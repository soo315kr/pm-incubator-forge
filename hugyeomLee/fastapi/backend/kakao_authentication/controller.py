"""
Kakao 인증 Controller.
요청 전달 및 응답 반환만 수행하며, 환경 변수·기본값·URL/토큰 구성 로직은 Service에 위임한다.
"""

from typing import Optional, Union

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse

from kakao_authentication.schemas import AccessTokenResult, OAuthLinkResponse
from kakao_authentication.service_interface import KakaoAuthenticationServiceInterface
from kakao_authentication.service_impl import KakaoAuthenticationServiceImpl


def get_kakao_auth_service() -> KakaoAuthenticationServiceInterface:
    """Service Interface 구현체를 반환 (DI). Controller는 인터페이스에만 의존한다."""
    return KakaoAuthenticationServiceImpl()


router = APIRouter()


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 생성 (PM-EDDI-2)",
)
def request_oauth_link(
    service: KakaoAuthenticationServiceInterface = Depends(get_kakao_auth_service),
) -> OAuthLinkResponse:
    """
    사용자가 Kakao 인증 요청 시 인증 URL을 즉시 반환한다.
    생성된 URL은 Kakao OAuth 기준에 맞는 필수 파라미터를 포함한다.
    """
    try:
        return service.get_oauth_authorization_url()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/request-access-token-after-redirection",
    response_model=AccessTokenResult,
    summary="인가 코드로 액세스 토큰 발급 및 사용자 정보 조회 (PM-EDDI-3, PM-EDDI-4)",
    responses={307: {"description": "code 누락 시 Kakao 인증 페이지로 리다이렉트"}},
)
def request_access_token_after_redirection(
    code: Optional[str] = Query(None, description="Kakao 인증 후 전달된 인가 코드"),
    error: Optional[str] = Query(None, description="Kakao OAuth 오류 코드 (인증 거부 시 등)"),
    error_description: Optional[str] = Query(None, description="Kakao OAuth 오류 상세 메시지"),
    service: KakaoAuthenticationServiceInterface = Depends(get_kakao_auth_service),
) -> Union[AccessTokenResult, RedirectResponse]:
    """
    인가 코드(code)를 받아 Kakao 액세스 토큰을 발급하고, 해당 토큰으로 사용자 정보를 조회하여 반환한다.
    code가 없으면 Kakao 인증 페이지로 자동 리다이렉트한다.
    """
    if error:
        raise HTTPException(
            status_code=400,
            detail=error_description or f"Kakao 인증 실패: {error}",
        )
    if not code or not code.strip():
        # code가 없으면 Kakao 인증 페이지로 리다이렉트
        oauth_link = service.get_oauth_authorization_url()
        return RedirectResponse(url=oauth_link.url, status_code=307)
    try:
        return service.request_access_token_after_redirection(code=code.strip())
    except httpx.HTTPStatusError as e:
        detail = "인가 코드가 잘못되었거나 만료되었습니다."
        if e.response.text:
            try:
                body = e.response.json()
                detail = body.get("error_description", body.get("error", detail))
            except Exception:
                pass
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
