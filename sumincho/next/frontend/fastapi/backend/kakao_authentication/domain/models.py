"""Domain models for Kakao authentication."""
from typing import Optional
from pydantic import BaseModel


class OAuthLinkRequest(BaseModel):
    """Request model for OAuth link generation."""
    pass


class OAuthLinkResponse(BaseModel):
    """Response model for OAuth link generation."""
    oauth_url: str


class AccessTokenRequest(BaseModel):
    """Request model for access token generation."""
    code: str


class AccessTokenResponse(BaseModel):
    """Response model for access token generation."""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None


class KakaoUserInfo(BaseModel):
    """Kakao user information model."""
    id: int
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image: Optional[str] = None


class AccessTokenWithUserInfoResponse(BaseModel):
    """Response model for access token with user info."""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    user_info: KakaoUserInfo
