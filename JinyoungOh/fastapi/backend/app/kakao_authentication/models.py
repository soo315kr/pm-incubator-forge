"""Kakao OAuth 도메인 모델."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class KakaoUserInfo:
    """Kakao 사용자 정보 (API /v2/user/me 응답 매핑)."""

    id: int
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image_url: Optional[str] = None
    thumbnail_image_url: Optional[str] = None


@dataclass
class TokenResponse:
    """액세스 토큰 발급 API 응답. user_info는 PM-EDDI-4 연동 시 채워진다."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    user_info: Optional["KakaoUserInfo"] = None
