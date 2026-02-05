"""카카오 인증 라우팅. URL → Controller 연결만 수행."""
from fastapi import APIRouter, Depends, Query

from config import Settings, get_settings
from kakao_authentication.controller import (
    login_page as login_page_handler,
    request_oauth_link as request_oauth_link_handler,
    request_access_token_after_redirection as request_access_token_handler,
)
from kakao_authentication.service import KakaoAuthService, KakaoAuthServiceImpl

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])


def get_kakao_service(settings: Settings = Depends(get_settings)) -> KakaoAuthService:
    return KakaoAuthServiceImpl(settings)


@router.get("/login")
def login_page(service: KakaoAuthService = Depends(get_kakao_service)):
    return login_page_handler(service)


@router.get("/request-oauth-link")
def request_oauth_link(service: KakaoAuthService = Depends(get_kakao_service)):
    return request_oauth_link_handler(service)


@router.get("/request-access-token-after-redirection")
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 발급된 인가 코드"),
    service: KakaoAuthService = Depends(get_kakao_service),
):
    return await request_access_token_handler(code, service)
