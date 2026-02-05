"""
Kakao 인증 서비스 인터페이스
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class KakaoAuthServiceInterface(ABC):
    """Kakao 인증 서비스 인터페이스"""
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def request_access_token(
        self,
        code: str,
        client_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        grant_type: str = "authorization_code"
    ) -> Dict[str, any]:
        """
        인가 코드를 사용하여 Kakao 액세스 토큰을 요청하고 사용자 정보를 조회합니다.
        
        Args:
            code: 인가 코드
            client_id: Kakao Client ID (None인 경우 환경 변수에서 로드)
            redirect_uri: 리다이렉트 URI (None인 경우 환경 변수에서 로드)
            grant_type: Grant 타입 (기본값: "authorization_code")
        
        Returns:
            토큰 정보와 사용자 정보를 포함한 딕셔너리 (access_token, token_type, refresh_token, expires_in, user_info 등)
        
        Raises:
            ValueError: 필수 파라미터가 누락된 경우
            Exception: Kakao API 요청 실패 시
        """
        pass
    
    @abstractmethod
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
        pass
