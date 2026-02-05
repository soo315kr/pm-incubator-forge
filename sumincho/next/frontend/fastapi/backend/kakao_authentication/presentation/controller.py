"""Controller for Kakao authentication API endpoints."""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from kakao_authentication.domain.models import (
    AccessTokenRequest,
    AccessTokenResponse,
    AccessTokenWithUserInfoResponse,
    OAuthLinkRequest,
    OAuthLinkResponse,
)
from kakao_authentication.domain.service_interface import (
    KakaoAuthenticationServiceInterface,
)
from kakao_authentication.domain.service_impl import KakaoAuthenticationServiceImpl

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])

# Service instance (lazy initialization)
_service: Optional[KakaoAuthenticationServiceInterface] = None


def get_service() -> KakaoAuthenticationServiceInterface:
    """Get service instance (lazy initialization for dependency injection)."""
    global _service
    if _service is None:
        _service = KakaoAuthenticationServiceImpl()
    return _service


@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
async def request_oauth_link() -> OAuthLinkResponse:
    """
    Generate Kakao OAuth authentication URL.
    
    Returns:
        OAuth link response containing the authentication URL
    """
    try:
        service = get_service()
        request = OAuthLinkRequest()
        response = service.generate_oauth_link(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/request-access-token-after-redirection", response_model=AccessTokenWithUserInfoResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Authorization code from Kakao OAuth redirect")
) -> AccessTokenWithUserInfoResponse:
    """
    Request access token using authorization code and return with user information.
    
    Args:
        code: Authorization code received from Kakao OAuth redirect
        
    Returns:
        Access token response with user information
    """
    try:
        if not code:
            raise HTTPException(status_code=400, detail="Authorization code is required")
        
        service = get_service()
        request = AccessTokenRequest(code=code)
        response = service.request_access_token_with_user_info(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
