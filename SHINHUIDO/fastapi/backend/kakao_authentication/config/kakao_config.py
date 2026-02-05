"""
Kakao OAuth 설정 모듈

환경 변수에서 Kakao OAuth 관련 설정값을 로드합니다.
"""
import os
from typing import Optional


class KakaoConfig:
    """Kakao OAuth 설정 클래스"""
    
    @staticmethod
    def get_client_id() -> str:
        """Kakao OAuth Client ID를 반환합니다."""
        client_id = os.getenv("KAKAO_CLIENT_ID")
        if not client_id:
            raise ValueError("KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다.")
        return client_id
    
    @staticmethod
    def get_redirect_uri() -> str:
        """Kakao OAuth Redirect URI를 반환합니다."""
        redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
        if not redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI 환경 변수가 설정되지 않았습니다.")
        return redirect_uri
    
    @staticmethod
    def get_client_secret() -> Optional[str]:
        """Kakao OAuth Client Secret을 반환합니다 (선택사항)."""
        return os.getenv("KAKAO_CLIENT_SECRET")
    
    @staticmethod
    def get_token_url() -> str:
        """Kakao 토큰 발급 URL을 반환합니다."""
        return "https://kauth.kakao.com/oauth/token"
    
    @staticmethod
    def get_user_info_url() -> str:
        """Kakao 사용자 정보 조회 URL을 반환합니다."""
        return "https://kapi.kakao.com/v2/user/me"
    
    @staticmethod
    def get_auth_url() -> str:
        """Kakao 인증 URL을 반환합니다."""
        return "https://kauth.kakao.com/oauth/authorize"

