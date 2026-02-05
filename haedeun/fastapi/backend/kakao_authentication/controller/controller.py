"""
Kakao 인증 Controller

FastAPI 라우터를 통해 API 엔드포인트를 제공합니다.
Controller는 Service Interface에만 의존합니다.
"""
from fastapi import APIRouter, HTTPException, Query
import httpx
from kakao_authentication.models import (
    OAuthLinkResponse,
    AccessTokenResponse,
    UserInfoResponse
)
from kakao_authentication.service.service_interface import KakaoAuthenticationServiceInterface
from kakao_authentication.service.service_impl import KakaoAuthenticationService

# Service 인스턴스 생성 (의존성 주입을 위해 추후 개선 가능)
_service: KakaoAuthenticationServiceInterface = KakaoAuthenticationService()

# 라우터 생성
router = APIRouter()


@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
async def request_oauth_link() -> OAuthLinkResponse:
    """
    Kakao OAuth 인증 URL을 생성합니다.
    
    Returns:
        OAuthLinkResponse: 생성된 인증 URL
        
    Raises:
        HTTPException: 환경 변수 누락 또는 URL 생성 실패 시
    """
    try:
        return _service.generate_oauth_url()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인증 URL 생성 중 오류가 발생했습니다: {str(e)}")


@router.get("/request-access-token-after-redirection", response_model=AccessTokenResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 받은 인가 코드")
) -> AccessTokenResponse:
    """
    인가 코드를 받아 Kakao 액세스 토큰을 발급받습니다.
    
    Args:
        code: Kakao 인증 후 받은 인가 코드
        
    Returns:
        AccessTokenResponse: 발급된 액세스 토큰 정보
        
    Raises:
        HTTPException: 파라미터 누락 또는 토큰 발급 실패 시
    """
    try:
        return _service.request_access_token(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Kakao 토큰 발급 실패: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"액세스 토큰 발급 중 오류가 발생했습니다: {str(e)}")


@router.get("/user-info", response_model=UserInfoResponse)
async def get_user_info(
    access_token: str = Query(..., description="Kakao 액세스 토큰")
) -> UserInfoResponse:
    """
    액세스 토큰을 사용하여 Kakao 사용자 정보를 조회합니다.
    
    Args:
        access_token: Kakao 액세스 토큰
        
    Returns:
        UserInfoResponse: 사용자 정보
        
    Raises:
        HTTPException: 토큰 유효성 검증 실패 또는 API 오류 시
    """
    try:
        return _service.get_user_info(access_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Kakao 사용자 정보 조회 실패: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 정보 조회 중 오류가 발생했습니다: {str(e)}")
