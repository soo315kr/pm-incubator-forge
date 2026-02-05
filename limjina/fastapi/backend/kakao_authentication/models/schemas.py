"""
Kakao 인증 API 요청/응답 스키마.
PM-EDDI-3 토큰 발급 결과와 PM-EDDI-4 사용자 정보를 통합한 반환 값 정의.
"""
from typing import Optional

from pydantic import BaseModel, Field


# PM-EDDI-2: 인증 URL 응답
class OAuthLinkResponse(BaseModel):
    """GET /request-oauth-link 응답."""
    auth_url: str = Field(..., description="Kakao OAuth 인증 페이지 URL")


# PM-EDDI-3: 액세스 토큰 응답 (Kakao API 형식)
class TokenResponse(BaseModel):
    """Kakao 토큰 서버 응답."""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: Optional[int] = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간(초)")
    scope: Optional[str] = Field(None, description="동의한 scope")


# PM-EDDI-4: Kakao 사용자 정보
class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (Kakao API /v2/user/me 응답 기반)."""
    id: int = Field(..., description="Kakao 사용자 ID")
    connected_at: Optional[str] = Field(None, description="연결 시각")
    properties: Optional[dict] = Field(default_factory=dict, description="닉네임, 프로필 이미지 등")
    kakao_account: Optional[dict] = Field(default_factory=dict, description="이메일 등 계정 정보")


# PM-EDDI-3 + PM-EDDI-4 통합: 토큰 발급 + 사용자 정보
class TokenAndUserResponse(BaseModel):
    """
    PM-EDDI-3 토큰 발급 결과와 PM-EDDI-4 사용자 정보를 통합한 반환 값.
    GET /request-access-token-after-redirection 호출 시 토큰과 사용자 정보를 함께 반환.
    """
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: Optional[int] = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간(초)")
    user: KakaoUserInfo = Field(..., description="Kakao 사용자 정보")
