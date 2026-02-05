"""
Kakao 인증 서비스 구현체
"""
from typing import Dict, Optional
from urllib.parse import urlencode

import httpx

from config import get_env, get_env_required

from kakao_authentication.service.kakao_auth_service_interface import (
    KakaoAuthServiceInterface,
)


class KakaoAuthService(KakaoAuthServiceInterface):
    """Kakao 인증 서비스 구현체"""
    
    KAKAO_OAUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    def __init__(self):
        """서비스 초기화"""
        self._default_client_id = get_env("KAKAO_CLIENT_ID")
        self._default_redirect_uri = get_env("KAKAO_REDIRECT_URI")
    
    def generate_oauth_url(
        self,
        client_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        response_type: str = "code"
    ) -> str:
        """
        Kakao OAuth 인증 URL을 생성합니다.
        
        Args:
            client_id: Kakao Client ID (None인 경우 환경 변수에서 로드)
            redirect_uri: 리다이렉트 URI (None인 경우 환경 변수에서 로드)
            response_type: 응답 타입 (기본값: "code")
        
        Returns:
            생성된 OAuth 인증 URL
        
        Raises:
            ValueError: 필수 파라미터가 누락된 경우
        """
        # client_id 결정: 파라미터 우선, 없으면 환경 변수, 둘 다 없으면 에러
        final_client_id = client_id or self._default_client_id
        if not final_client_id:
            raise ValueError(
                "client_id is required. Provide it as a parameter or set KAKAO_CLIENT_ID environment variable."
            )
        
        # redirect_uri 결정: 파라미터 우선, 없으면 환경 변수, 둘 다 없으면 에러
        final_redirect_uri = redirect_uri or self._default_redirect_uri
        if not final_redirect_uri:
            raise ValueError(
                "redirect_uri is required. Provide it as a parameter or set KAKAO_REDIRECT_URI environment variable."
            )
        
        # response_type 검증
        if response_type not in ["code"]:
            raise ValueError(f"Invalid response_type: {response_type}. Must be 'code'.")
        
        # URL 파라미터 구성
        params = {
            "client_id": final_client_id,
            "redirect_uri": final_redirect_uri,
            "response_type": response_type,
        }
        
        # URL 생성
        oauth_url = f"{self.KAKAO_OAUTH_BASE_URL}?{urlencode(params)}"
        
        return oauth_url
    
    def request_access_token(
        self,
        code: str,
        client_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        grant_type: str = "authorization_code"
    ) -> Dict[str, any]:
        """
        인가 코드를 사용하여 Kakao 액세스 토큰을 요청합니다.
        
        Args:
            code: 인가 코드
            client_id: Kakao Client ID (None인 경우 환경 변수에서 로드)
            redirect_uri: 리다이렉트 URI (None인 경우 환경 변수에서 로드)
            grant_type: Grant 타입 (기본값: "authorization_code")
        
        Returns:
            토큰 정보를 포함한 딕셔너리 (access_token, token_type, refresh_token, expires_in 등)
        
        Raises:
            ValueError: 필수 파라미터가 누락된 경우
            Exception: Kakao API 요청 실패 시
        """
        # code 검증
        if not code:
            raise ValueError("code is required")
        
        # client_id 결정: 파라미터 우선, 없으면 환경 변수, 둘 다 없으면 에러
        final_client_id = client_id or self._default_client_id
        if not final_client_id:
            raise ValueError(
                "client_id is required. Provide it as a parameter or set KAKAO_CLIENT_ID environment variable."
            )
        
        # redirect_uri 결정: 파라미터 우선, 없으면 환경 변수, 둘 다 없으면 에러
        final_redirect_uri = redirect_uri or self._default_redirect_uri
        if not final_redirect_uri:
            raise ValueError(
                "redirect_uri is required. Provide it as a parameter or set KAKAO_REDIRECT_URI environment variable."
            )
        
        # grant_type 검증
        if grant_type != "authorization_code":
            raise ValueError(f"Invalid grant_type: {grant_type}. Must be 'authorization_code'.")
        
        # 요청 데이터 구성
        data = {
            "grant_type": grant_type,
            "client_id": final_client_id,
            "redirect_uri": final_redirect_uri,
            "code": code,
        }
        
        # Kakao 토큰 서버로 요청
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.KAKAO_TOKEN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10.0,
                )
                response.raise_for_status()
                token_data = response.json()
                
                # PM-EDDI-4: 액세스 토큰 발급 후 사용자 정보 조회
                access_token = token_data.get("access_token")
                if access_token:
                    try:
                        user_info = self.get_user_info(access_token)
                        token_data["user_info"] = user_info
                    except Exception as e:
                        # 사용자 정보 조회 실패해도 토큰은 반환 (경고만 기록)
                        print(f"Warning: Failed to fetch user info: {str(e)}")
                
                return token_data
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_response = e.response.json()
                error_detail = error_response.get("error_description", str(e))
            except:
                error_detail = str(e)
            raise Exception(f"Failed to request access token from Kakao: {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to Kakao API: {str(e)}")
    
    def get_user_info(self, access_token: str) -> Dict[str, any]:
        """
        액세스 토큰을 사용하여 Kakao 사용자 정보를 조회합니다.
        
        Args:
            access_token: Kakao 액세스 토큰
        
        Returns:
            사용자 정보를 포함한 딕셔너리 (id, kakao_account 등)
        
        Raises:
            ValueError: 액세스 토큰이 유효하지 않은 경우
            Exception: Kakao API 요청 실패 시
        """
        if not access_token:
            raise ValueError("access_token is required")
        
        # Kakao 사용자 정보 API로 요청
        try:
            with httpx.Client() as client:
                response = client.get(
                    self.KAKAO_USER_INFO_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                user_info = response.json()
                
                return user_info
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_response = e.response.json()
                error_detail = error_response.get("msg", error_response.get("error_description", str(e)))
            except:
                error_detail = str(e)
            
            if e.response.status_code == 401:
                raise ValueError(f"Invalid or expired access token: {error_detail}")
            raise Exception(f"Failed to fetch user info from Kakao: {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to Kakao API: {str(e)}")
