"""
Kakao 인증 Controller.
요청 전달 및 응답 반환만 수행하며, 환경 변수·URL 구성 로직은 다루지 않는다.
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from kakao_authentication.exceptions import (
    KakaoOAuthConfigError,
    KakaoTokenError,
    KakaoUserInfoError,
)
from kakao_authentication.service_interface import KakaoAuthServiceInterface

router = APIRouter(tags=["kakao-authentication"])


def get_kakao_auth_service() -> KakaoAuthServiceInterface:
    """Service 구현체를 반환. Controller는 인터페이스에만 의존한다."""
    from kakao_authentication.service import KakaoAuthService

    return KakaoAuthService()


@router.get("/request-oauth-link")
def request_oauth_link(
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> dict:
    """
    Kakao OAuth 인증 URL을 생성하여 반환한다.
    사용자는 반환된 URL로 Kakao 인증 페이지로 이동할 수 있다.
    """
    try:
        url = service.get_authorization_url()
        return {"url": url}
    except KakaoOAuthConfigError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/request-access-token-after-redirection")
def request_access_token_after_redirection(
    code: str | None = Query(None, description="Kakao 인증 후 리다이렉트로 받은 인가 코드"),
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> dict:
    """
    인가 코드(code)를 받아 Kakao 액세스 토큰·리프레시 토큰을 발급받는다.
    Kakao 인증 후 리다이렉트된 URL의 query parameter `code`를 전달한다.
    """
    try:
        if not code:
            raise HTTPException(
                status_code=400,
                detail="인가 코드(code)가 누락되었습니다. 쿼리 파라미터 code를 포함해 요청해 주세요.",
            )
        result = service.exchange_code_for_tokens(code)
        return {
            "access_token": result.access_token,
            "token_type": result.token_type,
            "refresh_token": result.refresh_token,
            "expires_in": result.expires_in,
            "refresh_token_expires_in": result.refresh_token_expires_in,
            "scope": result.scope,
            "user": {
                "id": result.user.id,
                "nickname": result.user.nickname,
                "email": result.user.email,
                "profile_image_url": result.user.profile_image_url,
                "thumbnail_image_url": result.user.thumbnail_image_url,
            },
        }
    except KakaoOAuthConfigError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except KakaoTokenError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except KakaoUserInfoError as e:
        raise HTTPException(status_code=400, detail=e.message)
