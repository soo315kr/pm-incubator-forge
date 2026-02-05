"""Kakao 인증 API 요청/응답 스키마."""

from pydantic import BaseModel, Field


class OAuthLinkResponse(BaseModel):
    """PM-EDDI-2: 인증 URL 생성 API 응답."""

    url: str = Field(..., description="Kakao OAuth 인증 페이지 URL")


class KakaoUserInfo(BaseModel):
    """PM-EDDI-4: Kakao 사용자 정보 (id, 닉네임, 이메일 등)."""

    id: int = Field(..., description="Kakao 사용자 ID")
    nickname: str | None = Field(None, description="닉네임")
    email: str | None = Field(None, description="이메일 (동의 시)")
    profile_image_url: str | None = Field(None, description="프로필 이미지 URL")


class TokenWithUserInfoResponse(BaseModel):
    """PM-EDDI-3/4: 액세스 토큰 발급 + 사용자 정보 통합 응답."""

    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    expires_in: int | None = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token: str | None = Field(None, description="리프레시 토큰")
    refresh_token_expires_in: int | None = Field(None, description="리프레시 토큰 만료 시간(초)")
    user: KakaoUserInfo = Field(..., description="Kakao 사용자 정보")
