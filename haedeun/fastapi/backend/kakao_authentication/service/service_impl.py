"""
Kakao 인증 Service 구현체

KakaoAuthenticationServiceInterface의 구현체입니다.
"""
import os
from urllib.parse import urlencode
import httpx
from kakao_authentication.models import (
    OAuthLinkResponse,
    AccessTokenResponse,
    UserInfoResponse
)
from kakao_authentication.service.service_interface import KakaoAuthenticationServiceInterface


class KakaoAuthenticationService(KakaoAuthenticationServiceInterface):
    """Kakao 인증 Service 구현체"""
    
    # Kakao OAuth 설정
    KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    def __init__(self):
        """Service 초기화 및 환경 변수 검증"""
        self.client_id = os.getenv("KAKAO_CLIENT_ID")
        self.redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
        
        if not self.client_id:
            raise ValueError("KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다.")
        if not self.redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI 환경 변수가 설정되지 않았습니다.")
    
    def generate_oauth_url(self) -> OAuthLinkResponse:
        """
        Kakao OAuth 인증 URL을 생성합니다.
        
        Returns:
            OAuthLinkResponse: 생성된 인증 URL을 포함한 응답
        """
        # Kakao OAuth 파라미터 구성
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code"
        }
        
        # URL 생성
        auth_url = f"{self.KAKAO_AUTH_URL}?{urlencode(params)}"
        
        return OAuthLinkResponse(auth_url=auth_url)
    
    def request_access_token(self, code: str) -> AccessTokenResponse:
        """
        인가 코드를 사용하여 Kakao 액세스 토큰을 발급받습니다.
        
        Args:
            code: Kakao 인증 후 받은 인가 코드
            
        Returns:
            AccessTokenResponse: 발급된 액세스 토큰 정보
            
        Raises:
            ValueError: 인가 코드가 누락된 경우
            Exception: Kakao API 요청 실패 시
        """
        if not code:
            raise ValueError("인가 코드(code)가 필요합니다.")
        
        # Kakao 토큰 요청 파라미터
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        
        # Kakao 토큰 서버로 요청
        with httpx.Client() as client:
            response = client.post(
                self.KAKAO_TOKEN_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data
            )
            response.raise_for_status()
            token_data = response.json()
        
        return AccessTokenResponse(
            access_token=token_data.get("access_token"),
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            scope=token_data.get("scope"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in")
        )
    
    def get_user_info(self, access_token: str) -> UserInfoResponse:
        """
        액세스 토큰을 사용하여 Kakao 사용자 정보를 조회합니다.
        
        Args:
            access_token: Kakao 액세스 토큰
            
        Returns:
            UserInfoResponse: 사용자 정보
            
        Raises:
            ValueError: 액세스 토큰이 유효하지 않은 경우
            Exception: Kakao API 요청 실패 시
        """
        if not access_token:
            raise ValueError("액세스 토큰이 필요합니다.")
        
        # Kakao 사용자 정보 API 요청
        with httpx.Client() as client:
            response = client.get(
                self.KAKAO_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            user_data = response.json()
        
        # Kakao API 응답 파싱
        kakao_account = user_data.get("kakao_account", {})
        properties = user_data.get("properties", {})
        
        return UserInfoResponse(
            id=user_data.get("id"),
            nickname=properties.get("nickname"),
            email=kakao_account.get("email"),
            profile_image=properties.get("profile_image")
        )
