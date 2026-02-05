"""Kakao 인증 Controller. Service 인터페이스에만 의존하며 요청 전달 및 응답 반환만 수행한다."""

from fastapi import APIRouter, Query

from kakao_authentication.exceptions import KakaoAuthenticationError
from kakao_authentication.schemas import OAuthLinkResponse, TokenWithUserResponse
from kakao_authentication.service_impl import KakaoAuthenticationServiceImpl
from kakao_authentication.service_interface import KakaoAuthenticationServiceInterface

router = APIRouter()

# Controller는 인터페이스 타입으로 의존; 구체 구현체는 한 곳에서 주입
_service: KakaoAuthenticationServiceInterface = KakaoAuthenticationServiceImpl()


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao 인증 URL 생성",
    description="Kakao OAuth 인증 페이지로 이동할 URL을 반환합니다. client_id, redirect_uri는 환경 변수에서 로드됩니다.",
)
def request_oauth_link() -> OAuthLinkResponse:
    return _service.get_oauth_link()


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenWithUserResponse,
    summary="인가 코드로 액세스 토큰 발급 및 사용자 정보 조회",
    description="Kakao 인증 후 받은 인가 코드(code)로 액세스 토큰을 발급하고, 해당 토큰으로 사용자 정보를 조회하여 함께 반환합니다.",
)
def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 리다이렉트된 URL의 query parameter 'code'"),
) -> TokenWithUserResponse:
    return _service.request_access_token_after_redirection(code)


def register_kakao_exception_handler(app):
    """KakaoAuthenticationError를 HTTP 응답으로 변환하는 예외 핸들러 등록."""
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(KakaoAuthenticationError)
    def kakao_auth_exception_handler(request: Request, exc: KakaoAuthenticationError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
    return app
