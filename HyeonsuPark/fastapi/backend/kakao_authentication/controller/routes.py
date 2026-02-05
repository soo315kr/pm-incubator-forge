"""Kakao 인증 Controller. 요청 전달 및 응답 반환만 수행하며 Service Interface에만 의존한다."""

from fastapi import APIRouter, Depends, HTTPException

from kakao_authentication.models import (
    KakaoAuthenticationError,
    OAuthLinkResponse,
    TokenWithUserResponse,
)
from kakao_authentication.service import (
    KakaoAuthServiceInterface,
    get_kakao_auth_service,
)

router = APIRouter()


def _handle_kakao_error(exc: KakaoAuthenticationError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 발급",
    description="Kakao 로그인 페이지로 이동할 수 있는 인증 URL을 반환합니다.",
)
def request_oauth_link(
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> OAuthLinkResponse:
    """사용자가 Kakao 인증 요청 시 인증 URL을 생성하여 반환한다."""
    try:
        oauth_url = service.get_oauth_authorize_url()
        return OAuthLinkResponse(oauth_url=oauth_url)
    except KakaoAuthenticationError as e:
        _handle_kakao_error(e)


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenWithUserResponse,
    summary="인가 코드로 액세스 토큰 및 사용자 정보 발급",
    description="Kakao 인증 후 받은 인가 코드(code)로 액세스 토큰과 사용자 정보를 요청합니다.",
)
def request_access_token_after_redirection(
    code: str,
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> TokenWithUserResponse:
    """인가 코드를 받아 액세스 토큰을 요청하고, 사용자 정보와 함께 반환한다."""
    try:
        return service.request_access_token_after_redirection(code)
    except KakaoAuthenticationError as e:
        _handle_kakao_error(e)
