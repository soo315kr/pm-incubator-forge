"""Kakao 인증 API 요청/응답 스키마."""
from typing import Optional

from pydantic import BaseModel, Field


class OAuthLinkResponse(BaseModel):
    """인증 URL 생성 API 응답."""
    url: str = Field(..., description="Kakao OAuth 인증 페이지 URL")


class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (PM-CHELSEA-4)."""
    id: int = Field(..., description="Kakao 사용자 ID")
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image_url: Optional[str] = None


class TokenAndUserResponse(BaseModel):
    """액세스 토큰 + 사용자 정보 응답 (PM-CHELSEA-3 + PM-CHELSEA-4 통합)."""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token_expires_in: Optional[int] = None
    user: Optional[KakaoUserInfo] = None
