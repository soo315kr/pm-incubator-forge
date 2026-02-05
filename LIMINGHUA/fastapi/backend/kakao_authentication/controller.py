import httpx
from fastapi import APIRouter, Depends, HTTPException

from kakao_authentication.schemas import OAuthLinkResponse, TokenWithUserResponse
from kakao_authentication.service_interface import KakaoAuthServiceInterface
from kakao_authentication.service_impl import KakaoAuthServiceImpl

router = APIRouter()


def get_kakao_auth_service() -> KakaoAuthServiceInterface:
    return KakaoAuthServiceImpl()


@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
def request_oauth_link(
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> OAuthLinkResponse:
    """Return Kakao OAuth authorization URL. User can open this URL to start Kakao login."""
    try:
        return service.get_oauth_link()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/request-access-token-after-redirection", response_model=TokenWithUserResponse)
def request_access_token_after_redirection(
    code: str,
    service: KakaoAuthServiceInterface = Depends(get_kakao_auth_service),
) -> TokenWithUserResponse:
    """Exchange authorization code for access token and return token with user info."""
    if not code or not code.strip():
        raise HTTPException(status_code=400, detail="Authorization code is required")
    try:
        return service.exchange_code_for_token_and_user(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except httpx.HTTPStatusError as e:
        body = e.response.text if e.response else ""
        raise HTTPException(
            status_code=e.response.status_code if e.response else 502,
            detail=body or "Kakao token request failed",
        ) from e
