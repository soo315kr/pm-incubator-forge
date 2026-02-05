"""
PM-EDDI-2, PM-EDDI-3, PM-EDDI-4: Kakao 인증 Service Interface
- Controller는 이 인터페이스에만 의존하며, 구현체에 직접 의존하지 않는다.
"""
from abc import ABC, abstractmethod

from kakao_authentication.dto.schemas import AccessTokenWithUserResponse


class KakaoAuthServiceInterface(ABC):
    """Kakao 인증 서비스 인터페이스 (Layered Architecture)"""

    @abstractmethod
    def get_authorization_url(self) -> str:
        """PM-EDDI-2: Kakao OAuth 인증 URL을 생성하여 반환한다."""
        ...

    @abstractmethod
    def request_access_token_after_redirection(self, code: str) -> AccessTokenWithUserResponse:
        """PM-EDDI-3: 인가 코드로 액세스 토큰을 요청하고, PM-EDDI-4에 따라 사용자 정보를 함께 반환한다."""
        ...
