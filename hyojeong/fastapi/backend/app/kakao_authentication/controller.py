from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from .dependencies import get_kakao_authentication_service
from .schemas import KakaoUserInfo, OAuthLinkResponse, TokenResponse
from .service import KakaoAuthenticationService

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])

@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
def request_oauth_link(
    service: KakaoAuthenticationService = Depends(get_kakao_authentication_service),
) -> OAuthLinkResponse:
    try:
        oauth_url = service.build_oauth_link()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return OAuthLinkResponse(oauth_url=oauth_url)


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenResponse,
)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao authorization code"),
    service: KakaoAuthenticationService = Depends(get_kakao_authentication_service),
) -> TokenResponse:
    try:
        return await service.request_access_token(code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/user-info", response_model=KakaoUserInfo)
async def request_user_info(
    access_token: str = Query(..., description="Kakao access token"),
    service: KakaoAuthenticationService = Depends(get_kakao_authentication_service),
) -> KakaoUserInfo:
    try:
        return await service.fetch_user_info(access_token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
