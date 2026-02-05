"""
Kakao 인증 컨트롤러
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from kakao_authentication.service.kakao_auth_service_interface import (
    KakaoAuthServiceInterface,
)
from kakao_authentication.service.kakao_auth_service import KakaoAuthService

# Router 생성
router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])

# Service 인스턴스 생성 (의존성 주입을 위해 나중에 개선 가능)
_service: Optional[KakaoAuthServiceInterface] = None


def get_service() -> KakaoAuthServiceInterface:
    """
    Service 인스턴스를 반환합니다.
    싱글톤 패턴을 사용합니다.
    """
    global _service
    if _service is None:
        _service = KakaoAuthService()
    return _service


@router.get("/request-oauth-link")
async def request_oauth_link(
    client_id: Optional[str] = Query(None, description="Kakao Client ID"),
    redirect_uri: Optional[str] = Query(None, description="리다이렉트 URI"),
    response_type: str = Query("code", description="응답 타입"),
) -> dict:
    """
    Kakao OAuth 인증 URL을 생성합니다.
    
    Args:
        client_id: Kakao Client ID (선택, 환경 변수에서도 로드 가능)
        redirect_uri: 리다이렉트 URI (선택, 환경 변수에서도 로드 가능)
        response_type: 응답 타입 (기본값: "code")
    
    Returns:
        생성된 OAuth 인증 URL을 포함한 응답
    
    Raises:
        HTTPException: 필수 파라미터가 누락되거나 잘못된 요청인 경우
    """
    try:
        service = get_service()
        oauth_url = service.generate_oauth_url(
            client_id=client_id,
            redirect_uri=redirect_uri,
            response_type=response_type,
        )
        
        return {
            "oauth_url": oauth_url,
            "message": "OAuth URL generated successfully",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/request-access-token-after-redirection")
async def request_access_token_after_redirection(
    code: str = Query(..., description="인가 코드"),
    client_id: Optional[str] = Query(None, description="Kakao Client ID"),
    redirect_uri: Optional[str] = Query(None, description="리다이렉트 URI"),
    grant_type: str = Query("authorization_code", description="Grant 타입"),
) -> dict:
    """
    인가 코드를 사용하여 Kakao 액세스 토큰을 요청하고 사용자 정보를 조회합니다.
    
    Args:
        code: 인가 코드 (필수)
        client_id: Kakao Client ID (선택, 환경 변수에서도 로드 가능)
        redirect_uri: 리다이렉트 URI (선택, 환경 변수에서도 로드 가능)
        grant_type: Grant 타입 (기본값: "authorization_code")
    
    Returns:
        발급된 액세스 토큰, 리프레시 토큰 및 사용자 정보를 포함한 응답
    
    Raises:
        HTTPException: 필수 파라미터가 누락되거나 잘못된 요청인 경우
    """
    try:
        service = get_service()
        token_data = service.request_access_token(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            grant_type=grant_type,
        )
        
        response_data = {
            "access_token": token_data.get("access_token"),
            "token_type": token_data.get("token_type", "Bearer"),
            "refresh_token": token_data.get("refresh_token"),
            "expires_in": token_data.get("expires_in"),
            "refresh_token_expires_in": token_data.get("refresh_token_expires_in"),
            "scope": token_data.get("scope"),
            "message": "Access token issued successfully",
        }
        
        # PM-EDDI-4: 사용자 정보가 있으면 응답에 포함
        if "user_info" in token_data:
            response_data["user_info"] = token_data["user_info"]
        
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
