from kakao_authentication.service.kakao_auth_service_interface import KakaoAuthServiceInterface
from kakao_authentication.service.kakao_auth_service_impl import KakaoAuthServiceImpl


def get_kakao_auth_service() -> KakaoAuthServiceInterface:
    """Service Interface를 반환한다. 구현체는 여기서만 결정된다."""
    return KakaoAuthServiceImpl()


__all__ = ["KakaoAuthServiceInterface", "KakaoAuthServiceImpl", "get_kakao_auth_service"]
