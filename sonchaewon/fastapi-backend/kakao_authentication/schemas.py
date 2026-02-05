"""Kakao 인증 API 요청/응답 스키마."""

from pydantic import BaseModel, Field


class OAuthLinkResponse(BaseModel):
    """인증 URL 생성 API 응답."""

    url: str = Field(..., description="Kakao OAuth 인증 페이지 URL")


class TokenAndUserResponse(BaseModel):
    """액세스 토큰 및 사용자 정보 응답 (PM-SCW-3 + PM-SCW-4 통합)."""

    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: str | None = Field(None, description="리프레시 토큰")
    expires_in: int = Field(..., description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: int | None = Field(None, description="리프레시 토큰 만료 시간(초)")
    user: "KakaoUserInfo" = Field(..., description="Kakao 사용자 정보")


class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (PM-SCW-4)."""

    id: int = Field(..., description="Kakao 사용자 ID")
    nickname: str | None = Field(None, description="닉네임")
    email: str | None = Field(None, description="이메일 (동의 시)")


TokenAndUserResponse.model_rebuild()
