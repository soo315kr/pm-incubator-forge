"""Kakao 인증 Controller. Service Interface에만 의존하며 요청 전달 및 응답 반환만 수행한다."""

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.kakao_authentication.schemas import OAuthLinkResponse, TokenWithUserInfoResponse
from app.kakao_authentication.service import (
    KakaoAuthenticationService,
    KakaoAuthenticationServiceImpl,
)


def get_kakao_authentication_service() -> KakaoAuthenticationService:
    """Service Interface 타입으로 구현체를 반환 (Controller는 구현체에 직접 의존하지 않음)."""
    return KakaoAuthenticationServiceImpl(
        client_id=settings.kakao_client_id,
        redirect_uri=settings.kakao_redirect_uri,
        client_secret=settings.kakao_client_secret,
        authorize_url=settings.kakao_authorize_url,
        token_url=settings.kakao_token_url,
        user_info_url=settings.kakao_user_info_url,
    )


router = APIRouter(
    prefix="/kakao-authentication",
    tags=["kakao-authentication"],
)


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 생성",
    description="PM-EDDI-2: 사용자가 Kakao 인증 요청 시 인증 URL을 반환한다.",
)
async def request_oauth_link(
    service: KakaoAuthenticationService = Depends(get_kakao_authentication_service),
) -> OAuthLinkResponse:
    """GET /kakao-authentication/request-oauth-link — 인증 URL을 즉시 반환한다."""
    try:
        url = service.get_oauth_authorize_url()
        return OAuthLinkResponse(url=url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"인증 URL 생성 실패: {e}")


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenWithUserInfoResponse,
    summary="인가 코드로 액세스 토큰 발급 및 사용자 정보 조회",
    description="PM-EDDI-3/4: 인가 코드(code)로 액세스 토큰을 요청하고, 발급된 토큰으로 사용자 정보를 조회하여 반환한다.",
)
async def request_access_token_after_redirection(
    code: str | None = None,
    service: KakaoAuthenticationService = Depends(get_kakao_authentication_service),
) -> TokenWithUserInfoResponse:
    """GET /kakao-authentication/request-access-token-after-redirection?code=..."""
    if not code:
        raise HTTPException(status_code=400, detail="필수 파라미터 code가 누락되었습니다.")
    try:
        return service.request_access_token_after_redirection(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"토큰/사용자 정보 처리 실패: {e}")
