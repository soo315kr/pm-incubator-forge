"""
의존성 주입: Service Interface에 구현체를 바인딩한다.
- Controller는 KakaoAuthServiceInterface 타입만 사용하며, 구현체를 알지 못한다.
"""
from config.env import get_kakao_config
from kakao_authentication.service.interface import KakaoAuthServiceInterface
from kakao_authentication.service.impl import KakaoAuthServiceImpl


def get_kakao_auth_service() -> KakaoAuthServiceInterface:
    """Controller가 의존하는 Service는 인터페이스 타입으로 제공되며, 실제 인스턴스는 구현체이다."""
    return KakaoAuthServiceImpl(config=get_kakao_config())
