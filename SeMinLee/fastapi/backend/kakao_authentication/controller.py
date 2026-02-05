"""
PM-EDDI-2, PM-EDDI-3: Kakao 인증 API Controller (Presentation Layer)
- Controller는 Service Interface에만 의존하며, 구현체를 직접 참조하지 않는다.
- 요청 전달 및 응답 반환만 수행한다. 환경 변수/URL 구성 로직은 Service에 있다.
"""
from fastapi import APIRouter, Depends, Query

from kakao_authentication.dto.schemas import OAuthLinkResponse, AccessTokenWithUserResponse
from kakao_authentication.service.interface import KakaoAuthServiceInterface
from kakao_authentication.di import get_kakao_auth_service

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 생성",
    description="PM-EDDI-2: 사용자가 Kakao 인증 요청 시 인증 URL을 반환합니다.",
)
def request_oauth_link(
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> OAuthLinkResponse:
    """GET /kakao-authentication/request-oauth-link — 인증 URL 즉시 반환."""
    url = service.get_authorization_url()
    return OAuthLinkResponse(url=url)


@router.get(
    "/request-access-token-after-redirection",
    response_model=AccessTokenWithUserResponse,
    summary="인가 코드로 액세스 토큰 및 사용자 정보 요청",
    description="PM-EDDI-3/PM-EDDI-4: 인가 코드(code)로 액세스 토큰을 발급하고 Kakao 사용자 정보를 함께 반환합니다.",
)
def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 전달된 인가 코드"),
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> AccessTokenWithUserResponse:
    """GET /kakao-authentication/request-access-token-after-redirection?code=... — 토큰 및 사용자 정보 반환."""
    return service.request_access_token_after_redirection(code=code)


