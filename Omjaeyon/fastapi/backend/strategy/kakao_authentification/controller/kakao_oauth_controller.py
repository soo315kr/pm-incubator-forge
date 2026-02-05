"""Controller for Kakao OAuth endpoints."""
from fastapi import APIRouter, HTTPException, Query
from strategy.kakao_authentification.service.kakao_oauth_service import KakaoOAuthServiceInterface
from strategy.kakao_authentification.service.kakao_oauth_service_impl import KakaoOAuthServiceImpl
from strategy.kakao_authentification.models.response import OAuthLinkResponse, AccessTokenResponse

router = APIRouter(prefix="/kakao-authentication", tags=["Kakao Authentication"])

# Service instance (in production, use dependency injection)
_service: KakaoOAuthServiceInterface = KakaoOAuthServiceImpl()


@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
async def request_oauth_link() -> OAuthLinkResponse:
    """
    Generate Kakao OAuth authorization URL.
    
    Returns:
        OAuthLinkResponse: Response containing the OAuth URL
        
    Raises:
        HTTPException: If OAuth URL generation fails
    """
    try:
        response = _service.generate_oauth_url()
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/request-access-token-after-redirection", response_model=AccessTokenResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Authorization code from Kakao OAuth callback")
) -> AccessTokenResponse:
    """
    Request access token from Kakao using authorization code.
    
    Args:
        code: Authorization code received from Kakao OAuth callback
        
    Returns:
        AccessTokenResponse: Response containing access token and related information
        
    Raises:
        HTTPException: If token request fails
    """
    if not code:
        raise HTTPException(
            status_code=400,
            detail="Authorization code is required"
        )
    
    try:
        response = _service.request_access_token(code)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
