"""
Kakao OAuth Service 구현체

Kakao OAuth 인증 관련 비즈니스 로직을 구현합니다.
"""
import httpx
from urllib.parse import urlencode
from typing import Dict, Any
from kakao_authentication.service.kakao_oauth_service_interface import KakaoOAuthServiceInterface
from kakao_authentication.models.kakao_oauth_models import (
    OAuthLinkResponse,
    AccessTokenResponse,
    AccessTokenWithUserInfoResponse,
    KakaoUserInfo
)
from kakao_authentication.config.kakao_config import KakaoConfig


class KakaoOAuthService(KakaoOAuthServiceInterface):
    """Kakao OAuth Service 구현체"""
    
    def __init__(self):
        """Service 초기화"""
        self.config = KakaoConfig()
    
    def generate_oauth_url(self) -> OAuthLinkResponse:
        """
        Kakao OAuth 인증 URL을 생성합니다.
        
        Returns:
            OAuthLinkResponse: 인증 URL을 포함한 응답 객체
            
        Raises:
            ValueError: 필수 환경 변수가 설정되지 않은 경우
        """
        client_id = self.config.get_client_id()
        redirect_uri = self.config.get_redirect_uri()
        auth_url_base = self.config.get_auth_url()
        
        # 필수 파라미터 검증
        if not client_id:
            raise ValueError("client_id가 설정되지 않았습니다.")
        if not redirect_uri:
            raise ValueError("redirect_uri가 설정되지 않았습니다.")
        
        # OAuth URL 파라미터 구성
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code"
        }
        
        # URL 생성
        auth_url = f"{auth_url_base}?{urlencode(params)}"
        
        return OAuthLinkResponse(auth_url=auth_url)
    
    def request_access_token(self, code: str) -> AccessTokenWithUserInfoResponse:
        """
        인가 코드를 사용하여 액세스 토큰을 요청하고 사용자 정보를 조회합니다.
        
        Args:
            code: Kakao 인증 후 발급된 인가 코드
            
        Returns:
            AccessTokenWithUserInfoResponse: 액세스 토큰과 사용자 정보를 포함한 응답 객체
            
        Raises:
            ValueError: 필수 파라미터가 누락된 경우
            Exception: Kakao API 요청 실패 시
        """
        # 필수 파라미터 검증
        if not code:
            raise ValueError("인가 코드(code)가 필요합니다.")
        
        # 액세스 토큰 요청
        access_token_response = self._request_token_from_kakao(code)
        
        # 사용자 정보 조회
        user_info = self._get_user_info(access_token_response.access_token)
        
        # 응답 객체 생성
        return AccessTokenWithUserInfoResponse(
            access_token=access_token_response.access_token,
            token_type=access_token_response.token_type,
            refresh_token=access_token_response.refresh_token,
            expires_in=access_token_response.expires_in,
            refresh_token_expires_in=access_token_response.refresh_token_expires_in,
            scope=access_token_response.scope,
            user_info=user_info
        )
    
    def _request_token_from_kakao(self, code: str) -> AccessTokenResponse:
        """
        Kakao 토큰 서버에 액세스 토큰을 요청합니다.
        
        Args:
            code: 인가 코드
            
        Returns:
            AccessTokenResponse: 액세스 토큰 응답
            
        Raises:
            Exception: Kakao API 요청 실패 시
        """
        client_id = self.config.get_client_id()
        redirect_uri = self.config.get_redirect_uri()
        client_secret = self.config.get_client_secret()
        token_url = self.config.get_token_url()
        
        # 요청 데이터 구성
        data: Dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code
        }
        
        # Client Secret이 있는 경우 추가
        if client_secret:
            data["client_secret"] = client_secret
        
        # Kakao 토큰 서버에 요청
        try:
            with httpx.Client() as client:
                response = client.post(
                    token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                token_data = response.json()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if e.response else str(e)
            raise Exception(f"Kakao 토큰 요청 실패: {error_detail}")
        except Exception as e:
            raise Exception(f"Kakao 토큰 요청 중 오류 발생: {str(e)}")
        
        # 응답 데이터 파싱
        return AccessTokenResponse(
            access_token=token_data.get("access_token"),
            token_type=token_data.get("token_type", "bearer"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
            scope=token_data.get("scope")
        )
    
    def _get_user_info(self, access_token: str) -> KakaoUserInfo:
        """
        액세스 토큰을 사용하여 Kakao 사용자 정보를 조회합니다.
        
        Args:
            access_token: 액세스 토큰
            
        Returns:
            KakaoUserInfo: 사용자 정보
            
        Raises:
            Exception: Kakao API 요청 실패 시
        """
        if not access_token:
            raise ValueError("액세스 토큰이 필요합니다.")
        
        user_info_url = self.config.get_user_info_url()
        
        try:
            with httpx.Client() as client:
                response = client.get(
                    user_info_url,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                response.raise_for_status()
                user_data = response.json()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if e.response else str(e)
            if e.response and e.response.status_code == 401:
                raise Exception(f"유효하지 않은 액세스 토큰입니다: {error_detail}")
            raise Exception(f"Kakao 사용자 정보 조회 실패: {error_detail}")
        except Exception as e:
            raise Exception(f"Kakao 사용자 정보 조회 중 오류 발생: {str(e)}")
        
        # 응답 데이터 파싱
        kakao_account = user_data.get("kakao_account", {})
        properties = kakao_account.get("profile", {})
        
        return KakaoUserInfo(
            id=user_data.get("id"),
            nickname=properties.get("nickname"),
            email=kakao_account.get("email"),
            profile_image=properties.get("profile_image_url")
        )

