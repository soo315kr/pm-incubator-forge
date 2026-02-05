"""Kakao 인증 Controller. Service Interface에만 의존하며 요청 전달 및 응답 반환만 수행한다."""

from fastapi import APIRouter, Depends, Query

from app.kakao_authentication.exceptions import InvalidAuthorizationCodeError
from app.kakao_authentication.schemas import OAuthLinkResponse, TokenWithUserResponse
from app.kakao_authentication.service_interface import KakaoAuthenticationServiceInterface
from app.kakao_authentication.service_impl import KakaoAuthenticationServiceImpl


def get_kakao_service() -> KakaoAuthenticationServiceInterface:
    """Service Interface를 반환하는 의존성. 구현체는 여기서만 바인딩된다."""
    return KakaoAuthenticationServiceImpl()


router = APIRouter()


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 생성",
    description="Kakao OAuth 인증 페이지로 이동할 URL을 반환합니다.",
)
def request_oauth_link(
    service: KakaoAuthenticationServiceInterface = Depends(get_kakao_service),
) -> OAuthLinkResponse:
    return service.get_oauth_link()


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenWithUserResponse,
    summary="인가 코드로 액세스 토큰 및 사용자 정보 발급",
    description="Kakao 인증 후 리다이렉트된 인가 코드(code)로 액세스 토큰과 사용자 정보를 발급받습니다.",
)
def request_access_token_after_redirection(
    code: str | None = Query(None, description="Kakao 인증 후 전달된 인가 코드"),
    service: KakaoAuthenticationServiceInterface = Depends(get_kakao_service),
) -> TokenWithUserResponse:
    if not code or not code.strip():
        raise InvalidAuthorizationCodeError("인가 코드(code)가 필요합니다. 쿼리 파라미터 code를 전달해 주세요.")
    return service.exchange_code_for_token_with_user(code)
