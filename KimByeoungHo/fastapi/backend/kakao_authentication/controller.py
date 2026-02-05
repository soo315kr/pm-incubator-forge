"""
Kakao Authentication Controller

PM-BH-2, 3, 4의 API 엔드포인트를 정의합니다.
Controller는 Service Interface에만 의존하며, 요청 전달 및 응답 반환만 수행합니다.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from kakao_authentication.service_interface import KakaoAuthenticationServiceInterface


# Router 생성
router = APIRouter(
    prefix="/kakao-authentication",
    tags=["Kakao Authentication"]
)


class KakaoAuthenticationController:
    """
    Kakao OAuth 인증 컨트롤러
    
    이 컨트롤러는 Service Interface에만 의존하며,
    HTTP 요청을 받아 Service로 전달하고 응답을 반환하는 역할만 수행합니다.
    """
    
    def __init__(self, service: KakaoAuthenticationServiceInterface):
        """
        Args:
            service: Kakao Authentication Service Interface 구현체
        """
        self.service = service
    
    async def request_oauth_link(self) -> Dict[str, str]:
        """
        PM-BH-2: Kakao OAuth 인증 URL을 생성하여 반환합니다.
        
        GET /kakao-authentication/request-oauth-link
        
        Returns:
            {
                "auth_url": "https://kauth.kakao.com/oauth/authorize?...",
                "client_id": "...",
                "redirect_uri": "...",
                "response_type": "code"
            }
        """
        try:
            oauth_url = self.service.generate_oauth_url()
            
            # Service 인스턴스에서 설정값 가져오기
            from kakao_authentication.service_implementation import KakaoAuthenticationService
            if isinstance(self.service, KakaoAuthenticationService):
                return {
                    "auth_url": oauth_url,
                    "client_id": self.service.client_id,
                    "redirect_uri": self.service.redirect_uri,
                    "response_type": "code"
                }
            else:
                # 인터페이스만 있는 경우 기본 응답
                return {"oauth_url": oauth_url}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"인증 URL 생성 실패: {str(e)}")
    
    async def request_access_token_after_redirection(
        self,
        code: str
    ) -> Dict[str, Any]:
        """
        PM-BH-3: 인가 코드로 Kakao 액세스 토큰을 요청합니다.
        
        GET /kakao-authentication/request-access-token-after-redirection?code={code}
        
        Args:
            code: Kakao로부터 받은 인가 코드 (Query Parameter)
            
        Returns:
            {
                "access_token": "...",
                "token_type": "bearer",
                "refresh_token": "...",
                "expires_in": 21599,
                "scope": "..."
            }
        """
        try:
            token_data = await self.service.request_access_token(code)
            return token_data
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"토큰 요청 실패: {str(e)}")
    
    async def get_user_info_with_token(
        self,
        access_token: str
    ) -> Dict[str, Any]:
        """
        PM-BH-4: 액세스 토큰으로 Kakao 사용자 정보를 조회합니다.
        
        GET /kakao-authentication/user-info?access_token={access_token}
        
        Args:
            access_token: Kakao 액세스 토큰 (Query Parameter)
            
        Returns:
            {
                "id": 123456789,
                "kakao_account": {
                    "profile": {"nickname": "..."},
                    "email": "..."
                }
            }
        """
        try:
            user_info = await self.service.get_user_info(access_token)
            return user_info
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"사용자 정보 조회 실패: {str(e)}")


def setup_routes(controller: KakaoAuthenticationController) -> APIRouter:
    """
    FastAPI Router에 엔드포인트를 등록합니다.
    
    Args:
        controller: KakaoAuthenticationController 인스턴스
        
    Returns:
        설정된 APIRouter
    """
    
    @router.get("/request-oauth-link")
    async def request_oauth_link():
        """PM-BH-2: Kakao OAuth 인증 URL 생성"""
        return await controller.request_oauth_link()
    
    @router.get("/callback")
    async def request_access_token(code: str = Query(..., description="인가 코드")):
        """PM-BH-3: 인가 코드로 액세스 토큰 요청"""
        return await controller.request_access_token_after_redirection(code)

    # 기존 Redirect URI 호환 (레거시 경로)
    @router.get("/request-access-token-after-redirection")
    async def request_access_token_legacy(code: str = Query(..., description="인가 코드")):
        """PM-BH-3: 인가 코드로 액세스 토큰 요청 (레거시 경로)"""
        return await controller.request_access_token_after_redirection(code)
    
    @router.get("/user-info")
    async def get_user_info(access_token: str = Query(..., description="액세스 토큰")):
        """PM-BH-4: 액세스 토큰으로 사용자 정보 조회"""
        return await controller.get_user_info_with_token(access_token)
    
    return router
