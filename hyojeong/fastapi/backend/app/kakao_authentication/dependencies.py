from __future__ import annotations

from .service import KakaoAuthenticationService
from .service_impl import KakaoAuthenticationServiceImpl


def get_kakao_authentication_service() -> KakaoAuthenticationService:
    return KakaoAuthenticationServiceImpl()
