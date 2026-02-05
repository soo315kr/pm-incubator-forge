"""
Kakao 인증 Service Interface

Service Interface는 추상 메서드를 정의하며,
Controller는 이 인터페이스에만 의존합니다.
"""
from abc import ABC, abstractmethod
from kakao_authentication.models import OAuthLinkResponse, AccessTokenResponse, UserInfoResponse


class KakaoAuthenticationServiceInterface(ABC):
    """Kakao 인증 Service Interface"""
    
    @abstractmethod
    def generate_oauth_url(self) -> OAuthLinkResponse:
        """
        Kakao OAuth 인증 URL을 생성합니다.
        
        Returns:
            OAuthLinkResponse: 생성된 인증 URL을 포함한 응답
            
        Raises:
            ValueError: 필수 환경 변수가 설정되지 않은 경우
        """
        pass
    
    @abstractmethod
    def request_access_token(self, code: str) -> AccessTokenResponse:
        """
        인가 코드를 사용하여 Kakao 액세스 토큰을 발급받습니다.
        
        Args:
            code: Kakao 인증 후 받은 인가 코드
            
        Returns:
            AccessTokenResponse: 발급된 액세스 토큰 정보
            
        Raises:
            ValueError: 필수 파라미터가 누락된 경우
            Exception: Kakao API 요청 실패 시
        """
        pass
    
    @abstractmethod
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
        pass
