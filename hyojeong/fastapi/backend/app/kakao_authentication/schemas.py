from __future__ import annotations

from pydantic import BaseModel


class OAuthLinkResponse(BaseModel):
    oauth_url: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    scope: str | None = None


class KakaoUserProfile(BaseModel):
    nickname: str | None = None


class KakaoUserAccount(BaseModel):
    email: str | None = None
    profile: KakaoUserProfile | None = None


class KakaoUserInfo(BaseModel):
    id: int
    nickname: str | None = None
    email: str | None = None
