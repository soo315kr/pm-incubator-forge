"""
Kakao OAuth Service Interface

Service 인터페이스를 정의하여 Controller가 구현체에 직접 의존하지 않도록 합니다.
"""
from abc import ABC, abstractmethod
from kakao_authentication.models.kakao_oauth_models import (
    OAuthLinkResponse,
    AccessTokenResponse,
    AccessTokenWithUserInfoResponse
)


class KakaoOAuthServiceInterface(ABC):
    """Kakao OAuth Service 인터페이스"""
    
    @abstractmethod
    def generate_oauth_url(self) -> OAuthLinkResponse:
        """
        Kakao OAuth 인증 URL을 생성합니다.
        
        Returns:
            OAuthLinkResponse: 인증 URL을 포함한 응답 객체
            
        Raises:
            ValueError: 필수 환경 변수가 설정되지 않은 경우
        """
        pass
    
    @abstractmethod
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
        pass

