"""요청/응답 스키마. 환경 변수·비즈니스 로직은 포함하지 않는다."""
from typing import Optional

from pydantic import BaseModel, Field


class OAuthLinkResponse(BaseModel):
    """인증 URL 생성 API 응답."""
    oauth_url: str = Field(..., description="Kakao OAuth 인증 페이지 URL")


class TokenResponse(BaseModel):
    """액세스 토큰 발급 API 응답 (PM-EDDI-3 + PM-EDDI-4 통합)."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    user: Optional["KakaoUserInfo"] = None


class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (동의 시 조회 가능)."""
    id: int = Field(..., description="Kakao 사용자 ID")
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image_url: Optional[str] = None
    thumbnail_image_url: Optional[str] = None


TokenResponse.model_rebuild()
