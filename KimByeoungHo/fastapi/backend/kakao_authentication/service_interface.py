"""
Kakao Authentication Service Interface

PM-BH-2, 3, 4의 아키텍처 요구사항에 따라 Service Interface를 정의합니다.
Controller는 이 인터페이스에만 의존하며, 구체적인 구현체는 알지 못합니다.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class KakaoAuthenticationServiceInterface(ABC):
    """
    Kakao OAuth 인증 서비스 인터페이스
    
    이 인터페이스는 Kakao OAuth 인증의 전체 플로우를 추상화합니다:
    1. 인증 URL 생성
    2. 액세스 토큰 발급
    3. 사용자 정보 조회
    """
    
    @abstractmethod
    def generate_oauth_url(self) -> str:
        """
        PM-BH-2: Kakao OAuth 인증 URL을 생성합니다.
        
        Returns:
            Kakao 인증 페이지 URL (client_id, redirect_uri, response_type 포함)
            
        Raises:
            ValueError: 필수 환경 변수가 누락된 경우
        """
        pass
    
    @abstractmethod
    async def request_access_token(self, code: str) -> Dict[str, Any]:
        """
        PM-BH-3: 인가 코드로 Kakao 액세스 토큰을 요청합니다.
        
        Args:
            code: Kakao로부터 받은 인가 코드
            
        Returns:
            액세스 토큰 정보를 포함한 딕셔너리:
            - access_token: 액세스 토큰
            - token_type: 토큰 타입 (예: "bearer")
            - refresh_token: 리프레시 토큰
            - expires_in: 만료 시간(초)
            - scope: 권한 범위
            
        Raises:
            ValueError: 잘못된 인가 코드 또는 파라미터
            RuntimeError: Kakao API 호출 실패
        """
        pass
    
    @abstractmethod
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        PM-BH-4: 액세스 토큰으로 Kakao 사용자 정보를 조회합니다.
        
        Args:
            access_token: PM-BH-3에서 발급받은 액세스 토큰
            
        Returns:
            사용자 정보를 포함한 딕셔너리:
            - id: Kakao 사용자 ID
            - kakao_account: 계정 정보
                - profile: 프로필 정보 (닉네임 등)
                - email: 이메일 (동의 시)
                
        Raises:
            ValueError: 유효하지 않은 액세스 토큰
            RuntimeError: Kakao API 호출 실패
        """
        pass
