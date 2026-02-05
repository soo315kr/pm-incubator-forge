"""
Kakao 인증 관련 데이터 모델
"""
from typing import Optional
from pydantic import BaseModel


class OAuthLinkResponse(BaseModel):
    """인증 URL 응답 모델"""
    auth_url: str


class AccessTokenRequest(BaseModel):
    """액세스 토큰 요청 모델"""
    code: str


class AccessTokenResponse(BaseModel):
    """액세스 토큰 응답 모델"""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None


class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 모델"""
    id: int
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image: Optional[str] = None


class TokenWithUserInfoResponse(BaseModel):
    """액세스 토큰과 사용자 정보를 포함한 응답 모델"""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    user_info: KakaoUserInfo
