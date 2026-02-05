"""
Kakao 인증 Controller.
요청 전달 및 응답 반환만 수행하며, 환경 변수/기본값/URL 구성 로직은 Service에 위임.
Service 인터페이스에만 의존한다.
"""
from fastapi import APIRouter, Depends, Query

from kakao_authentication.exceptions import (
    InvalidAuthorizationCodeError,
    InvalidRequestError,
    InvalidTokenError,
    KakaoApiError,
    KakaoAuthenticationError,
    MissingParameterError,
)
from kakao_authentication.models.schemas import OAuthLinkResponse, TokenAndUserResponse
from kakao_authentication.service import KakaoAuthServiceInterface, KakaoAuthServiceImpl


def get_kakao_auth_service() -> KakaoAuthServiceInterface:
    """Service 구현체를 반환 (DI). Controller는 인터페이스 타입만 사용."""
    return KakaoAuthServiceImpl()


router = APIRouter()


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 요청 (PM-EDDI-2)",
    description="Kakao OAuth 인증 페이지로 이동할 URL을 즉시 반환합니다. client_id, redirect_uri, response_type 등 필수 파라미터가 포함됩니다.",
)
def request_oauth_link(
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> OAuthLinkResponse:
    """GET /kakao-authentication/request-oauth-link — 인증 URL 생성."""
    return service.get_oauth_link()


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenAndUserResponse,
    summary="인가 코드로 액세스 토큰 및 사용자 정보 요청 (PM-EDDI-3 + PM-EDDI-4)",
    description="Kakao 인증 후 받은 인가 코드(code)로 액세스 토큰을 발급하고, 해당 토큰으로 사용자 정보를 조회하여 함께 반환합니다.",
)
def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 발급된 인가 코드"),
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> TokenAndUserResponse:
    """GET /kakao-authentication/request-access-token-after-redirection?code=..."""
    return service.request_access_token_and_user(code)


# 예외 핸들러 등록 (PM-EDDI-2, PM-EDDI-3, PM-EDDI-4 예외 처리)
def register_exception_handlers(application):
    """Kakao 인증 예외를 HTTP 응답으로 변환."""
    from fastapi.responses import JSONResponse

    @application.exception_handler(MissingParameterError)
    @application.exception_handler(InvalidRequestError)
    @application.exception_handler(InvalidAuthorizationCodeError)
    def handle_400(exc: KakaoAuthenticationError, _):
        return JSONResponse(status_code=400, content={"detail": exc.detail or exc.message})

    @application.exception_handler(InvalidTokenError)
    def handle_401(exc: KakaoAuthenticationError, _):
        return JSONResponse(status_code=401, content={"detail": exc.detail or exc.message})

    @application.exception_handler(KakaoApiError)
    def handle_kakao_api(exc: KakaoApiError, _):
        return JSONResponse(status_code=exc.status_code or 502, content={"detail": exc.detail or exc.message})
