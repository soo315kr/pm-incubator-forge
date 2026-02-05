"""
Kakao 인증 관련 데이터 모델
"""
from pydantic import BaseModel, HttpUrl


class OAuthLinkRequest(BaseModel):
    """인증 URL 생성 요청 모델"""
    pass  # GET 요청이므로 파라미터는 쿼리 파라미터로 받음


class OAuthLinkResponse(BaseModel):
    """인증 URL 생성 응답 모델"""
    auth_url: HttpUrl
    message: str = "Kakao 인증 URL이 생성되었습니다."


class AccessTokenRequest(BaseModel):
    """액세스 토큰 발급 요청 모델"""
    code: str


class AccessTokenResponse(BaseModel):
    """액세스 토큰 발급 응답 모델"""
    access_token: str
    token_type: str
    refresh_token: str | None = None
    expires_in: int
    scope: str | None = None
    refresh_token_expires_in: int | None = None


class UserInfoResponse(BaseModel):
    """사용자 정보 응답 모델"""
    id: int
    nickname: str | None = None
    email: str | None = None
    profile_image: str | None = None
