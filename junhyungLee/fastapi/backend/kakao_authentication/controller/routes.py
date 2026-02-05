"""Kakao 인증 API 라우트 (PM-EDDI-2). Controller는 Service Interface만 호출."""

from fastapi import APIRouter, Depends, HTTPException

from kakao_authentication.service.impl import KakaoAuthServiceImpl
from kakao_authentication.service.interface import KakaoAuthServiceProtocol

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])


def get_kakao_auth_service() -> KakaoAuthServiceProtocol:
    """Service Interface를 반환 (구현체는 여기서만 바인딩)."""
    return KakaoAuthServiceImpl()


@router.get("/request-oauth-link")
def request_oauth_link(
    service: KakaoAuthServiceProtocol = Depends(get_kakao_auth_service),
) -> dict:
    """Kakao OAuth 인증 URL을 반환한다 (GET)."""
    try:
        url = service.get_oauth_authorization_url()
        return {"oauth_link": url}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
