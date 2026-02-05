"""
Kakao Authentication Service Implementation

PM-BH-2, 3, 4의 실제 비즈니스 로직을 구현합니다.
환경 변수를 통해 설정값을 로드하고, Kakao OAuth API와 통신합니다.
"""
import os
from typing import Dict, Any
from urllib.parse import urlencode
import httpx

from kakao_authentication.service_interface import KakaoAuthenticationServiceInterface


class KakaoAuthenticationService(KakaoAuthenticationServiceInterface):
    """
    Kakao OAuth 인증 서비스 구현체
    
    환경 변수(.env)에서 Kakao OAuth 설정을 로드하고,
    Kakao API와 통신하여 인증 플로우를 처리합니다.
    """
    
    # Kakao OAuth 엔드포인트
    KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    def __init__(self):
        """
        서비스 초기화 시 환경 변수에서 설정값을 로드합니다.
        """
        self.client_id = os.getenv("KAKAO_CLIENT_ID")
        self.redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
        
        if not self.client_id:
            raise ValueError("KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다.")
        if not self.redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI 환경 변수가 설정되지 않았습니다.")
    
    def generate_oauth_url(self) -> str:
        """
        PM-BH-2: Kakao OAuth 인증 URL을 생성합니다.
        
        Kakao OAuth 기준에 맞게 client_id, redirect_uri, response_type을 포함합니다.
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code"
        }
        
        # URL 인코딩하여 전체 URL 생성
        query_string = urlencode(params)
        oauth_url = f"{self.KAKAO_AUTH_URL}?{query_string}"
        
        return oauth_url
    
    async def request_access_token(self, code: str) -> Dict[str, Any]:
        """
        PM-BH-3: 인가 코드로 Kakao 액세스 토큰을 요청합니다.
        
        Args:
            code: Kakao로부터 받은 인가 코드
            
        Returns:
            액세스 토큰 및 관련 정보
        """
        if not code:
            raise ValueError("인가 코드(code)가 제공되지 않았습니다.")
        
        # 토큰 요청 파라미터
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        
        # Kakao 토큰 서버에 요청
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.KAKAO_TOKEN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                
                token_data = response.json()
                return token_data
                
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.text else {}
                raise RuntimeError(
                    f"Kakao 토큰 요청 실패: {e.response.status_code}, "
                    f"상세: {error_detail}"
                )
            except Exception as e:
                raise RuntimeError(f"Kakao 토큰 요청 중 오류 발생: {str(e)}")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        PM-BH-4: 액세스 토큰으로 Kakao 사용자 정보를 조회합니다.
        
        Args:
            access_token: PM-BH-3에서 발급받은 액세스 토큰
            
        Returns:
            Kakao 사용자 정보
        """
        if not access_token:
            raise ValueError("액세스 토큰이 제공되지 않았습니다.")
        
        # Kakao 사용자 정보 API 요청
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.KAKAO_USER_INFO_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                    }
                )
                response.raise_for_status()
                
                user_info = response.json()
                return user_info
                
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.text else {}
                raise RuntimeError(
                    f"Kakao 사용자 정보 조회 실패: {e.response.status_code}, "
                    f"상세: {error_detail}"
                )
            except Exception as e:
                raise RuntimeError(f"Kakao 사용자 정보 조회 중 오류 발생: {str(e)}")
