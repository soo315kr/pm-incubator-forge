"""Kakao 인증 API 요청/응답 스키마."""

from pydantic import BaseModel, Field


class OAuthLinkResponse(BaseModel):
    """인증 URL 생성 API 응답."""

    oauth_link: str = Field(..., description="Kakao 인증 페이지로 이동할 URL")


class TokenResponse(BaseModel):
    """액세스 토큰 발급 API 응답 (PM-EDDI-3)."""

    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: str | None = Field(None, description="리프레시 토큰")
    expires_in: int | None = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: int | None = Field(None, description="리프레시 토큰 만료 시간(초)")


class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (PM-EDDI-4)."""

    id: int = Field(..., description="Kakao 사용자 ID")
    nickname: str | None = Field(None, description="닉네임")
    email: str | None = Field(None, description="이메일(동의 시)")


class TokenWithUserResponse(BaseModel):
    """액세스 토큰 + 사용자 정보 통합 응답 (PM-EDDI-3 + PM-EDDI-4)."""

    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: str | None = Field(None, description="리프레시 토큰")
    expires_in: int | None = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: int | None = Field(None, description="리프레시 토큰 만료 시간(초)")
    user: KakaoUserInfo = Field(..., description="Kakao 사용자 정보")
