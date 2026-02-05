from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class KakaoOAuthUrlResponse(BaseModel):
    """Kakao 인증 URL 응답 모델."""

    url: HttpUrl


class KakaoTokenResponse(BaseModel):
    """Kakao 액세스 토큰 응답 모델 (Kakao 기준 필드명 유지)."""

    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: int
    scope: Optional[str] = None
    refresh_token_expires_in: Optional[int] = None


class KakaoUserProfile(BaseModel):
    """Kakao 사용자 정보 응답 모델 (주요 필드만 매핑)."""

    id: int
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None


class KakaoTokenAndUserResponse(BaseModel):
    """PM-EDDI-3 + PM-EDDI-4 통합 응답: 토큰 + 사용자 정보."""

    token: KakaoTokenResponse
    user: KakaoUserProfile

