"""Response models for Kakao authentication."""
from pydantic import BaseModel
from typing import Optional


class OAuthLinkResponse(BaseModel):
    """Response model for OAuth link generation."""
    oauth_url: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "oauth_url": "https://kauth.kakao.com/oauth/authorize?client_id=xxx&redirect_uri=xxx&response_type=code"
            }
        }


class KakaoUserInfo(BaseModel):
    """Kakao user information model."""
    id: int
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 123456789,
                "nickname": "홍길동",
                "email": "user@example.com",
                "profile_image": "http://k.kakaocdn.net/..."
            }
        }


class AccessTokenResponse(BaseModel):
    """Response model for access token generation."""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    user_info: Optional[KakaoUserInfo] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "access_token_string",
                "token_type": "bearer",
                "refresh_token": "refresh_token_string",
                "expires_in": 21599,
                "scope": "profile_nickname profile_image account_email",
                "user_info": {
                    "id": 123456789,
                    "nickname": "홍길동",
                    "email": "user@example.com",
                    "profile_image": "http://k.kakaocdn.net/..."
                }
            }
        }
