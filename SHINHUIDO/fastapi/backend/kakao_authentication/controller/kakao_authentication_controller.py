"""
Kakao 인증 Controller

요청을 받아 Service Interface에 전달하고 응답을 반환하는 역할만 수행합니다.
"""
from fastapi import APIRouter, HTTPException, Query
from kakao_authentication.service.kakao_oauth_service_interface import KakaoOAuthServiceInterface
from kakao_authentication.service.kakao_oauth_service import KakaoOAuthService
from kakao_authentication.models.kakao_oauth_models import (
    OAuthLinkResponse,
    AccessTokenWithUserInfoResponse
)

router = APIRouter()

# Service 구현체 인스턴스 생성 (의존성 주입)
_service: KakaoOAuthServiceInterface = KakaoOAuthService()


@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
async def request_oauth_link() -> OAuthLinkResponse:
    """
    Kakao OAuth 인증 URL을 생성하여 반환합니다.
    
    Returns:
        OAuthLinkResponse: 인증 URL을 포함한 응답
        
    Raises:
        HTTPException: 환경 변수 누락 또는 URL 생성 실패 시
    """
    try:
        return _service.generate_oauth_url()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인증 URL 생성 실패: {str(e)}")


@router.get("/request-access-token-after-redirection", response_model=AccessTokenWithUserInfoResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 발급된 인가 코드")
) -> AccessTokenWithUserInfoResponse:
    """
    인가 코드를 받아 Kakao 액세스 토큰을 요청하고 사용자 정보를 조회합니다.
    
    Args:
        code: Kakao 인증 후 발급된 인가 코드
        
    Returns:
        AccessTokenWithUserInfoResponse: 액세스 토큰과 사용자 정보를 포함한 응답
        
    Raises:
        HTTPException: 파라미터 누락 또는 Kakao API 요청 실패 시
    """
    try:
        return _service.request_access_token(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

