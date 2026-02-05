"""
Kakao OAuth 관련 데이터 모델
"""
from pydantic import BaseModel, Field
from typing import Optional


class OAuthLinkResponse(BaseModel):
    """OAuth 인증 URL 응답 모델"""
    auth_url: str = Field(..., description="Kakao OAuth 인증 URL")


class AccessTokenRequest(BaseModel):
    """액세스 토큰 요청 모델"""
    code: str = Field(..., description="Kakao 인증 후 발급된 인가 코드")


class AccessTokenResponse(BaseModel):
    """액세스 토큰 응답 모델"""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(..., description="토큰 타입 (보통 'bearer')")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: Optional[int] = Field(None, description="토큰 만료 시간 (초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간 (초)")
    scope: Optional[str] = Field(None, description="토큰 권한 범위")


class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 모델"""
    id: int = Field(..., description="사용자 ID")
    nickname: Optional[str] = Field(None, description="닉네임")
    email: Optional[str] = Field(None, description="이메일 (동의 시)")
    profile_image: Optional[str] = Field(None, description="프로필 이미지 URL")


class AccessTokenWithUserInfoResponse(BaseModel):
    """액세스 토큰과 사용자 정보를 포함한 응답 모델"""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(..., description="토큰 타입")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: Optional[int] = Field(None, description="토큰 만료 시간 (초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간 (초)")
    scope: Optional[str] = Field(None, description="토큰 권한 범위")
    user_info: KakaoUserInfo = Field(..., description="사용자 정보")

