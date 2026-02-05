"""
kakao_authentication 도메인 DTO/스키마
- PM-EDDI-2: OAuth URL 응답
- PM-EDDI-3: 액세스 토큰 요청/응답
- PM-EDDI-4: 사용자 정보 (토큰 발급 결과와 통합)
"""
from typing import Optional

from pydantic import BaseModel, Field


# ----- PM-EDDI-2 -----
class OAuthLinkResponse(BaseModel):
    """GET /kakao-authentication/request-oauth-link 응답"""

    url: str = Field(..., description="Kakao OAuth 인증 URL")


# ----- PM-EDDI-3, PM-EDDI-4 -----
class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (PM-EDDI-4)"""

    id: Optional[str] = Field(None, description="Kakao 사용자 ID")
    nickname: Optional[str] = Field(None, description="닉네임")
    email: Optional[str] = Field(None, description="이메일 (동의 시)")


class AccessTokenWithUserResponse(BaseModel):
    """GET /kakao-authentication/request-access-token-after-redirection 응답 (PM-EDDI-3 + PM-EDDI-4)"""

    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: Optional[int] = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간(초)")
    user: Optional[KakaoUserInfo] = Field(None, description="Kakao 사용자 정보")
