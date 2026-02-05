"""Kakao 인증 Controller. 요청 전달 및 응답 반환만 수행하며 Service 인터페이스에만 의존한다."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse

from kakao_authentication.schemas import OAuthLinkResponse, TokenAndUserResponse
from kakao_authentication.service import KakaoAuthServiceInterface
from kakao_authentication.service_impl import KakaoAuthServiceImpl


def get_kakao_auth_service() -> KakaoAuthServiceInterface:
    """Service 구현체를 반환 (DI). Controller는 인터페이스 타입만 사용한다."""
    return KakaoAuthServiceImpl()


router = APIRouter()


@router.get(
    "/request-oauth-link",
    summary="Kakao OAuth 인증 URL 생성",
    description="카카오 인증 페이지로 즉시 리다이렉트합니다.",
)
def request_oauth_link(
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
):
    """사용자를 Kakao 인증 페이지로 즉시 보낸다."""
    try:
        # 1. 서비스로부터 링크 데이터를 먼저 가져옵니다.
        link_data = service.get_oauth_link()
        
        # 2. 가져온 데이터(link_data)의 url 속성을 사용하여 리다이렉트합니다.
        return RedirectResponse(url=link_data.url)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 예상치 못한 에러 발생 시 로그 출력
        print(f"Error in request_oauth_link: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenAndUserResponse,
    summary="인가 코드로 액세스 토큰 발급 및 사용자 정보 조회",
    description="Kakao 리다이렉트 후 받은 code로 액세스/리프레시 토큰을 발급하고 사용자 정보를 함께 반환합니다.",
)
def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 리다이렉트된 인가 코드"),
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> TokenAndUserResponse:
    """인가 코드(code)로 액세스 토큰을 발급받고, 해당 토큰으로 사용자 정보를 조회하여 반환한다."""
    try:
        return service.exchange_code_for_token_and_user(code=code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))