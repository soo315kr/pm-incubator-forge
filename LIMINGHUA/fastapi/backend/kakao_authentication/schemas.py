from pydantic import BaseModel, Field


class OAuthLinkResponse(BaseModel):
    url: str = Field(..., description="Kakao OAuth authorization URL")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None
    expires_in: int | None = None
    scope: str | None = None


class KakaoUserInfo(BaseModel):
    id: int
    nickname: str | None = None
    email: str | None = None
    profile_image_url: str | None = None


class TokenWithUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None
    expires_in: int | None = None
    scope: str | None = None
    user: KakaoUserInfo | None = None
