from pydantic import BaseModel, Field
from typing import Optional


class KakaoAuthUrlRequest(BaseModel):
    """Kakao 인증 URL 생성 요청"""
    redirect_uri: str = Field(..., description="리다이렉트 URI")
    client_id: Optional[str] = Field(None, description="Kakao 앱 REST API 키")
    response_type: str = Field(default="code", description="응답 타입")


class KakaoAuthUrlResponse(BaseModel):
    """Kakao 인증 URL 생성 응답"""
    auth_url: str = Field(..., description="Kakao 인증 URL")
    client_id: str = Field(..., description="사용된 클라이언트 ID")
    redirect_uri: str = Field(..., description="리다이렉트 URI")
    response_type: str = Field(..., description="응답 타입")


class KakaoTokenResponse(BaseModel):
    """Kakao 액세스 토큰 응답"""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(..., description="토큰 타입")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: int = Field(..., description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간(초)")
    scope: Optional[str] = Field(None, description="인가된 scope")


class KakaoUserInfoResponse(BaseModel):
    """Kakao 사용자 정보 응답"""
    id: int = Field(..., description="회원번호")
    nickname: Optional[str] = Field(None, description="닉네임")
    email: Optional[str] = Field(None, description="이메일")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")


class KakaoAuthCompleteResponse(BaseModel):
    """Kakao 인증 완료 응답 (토큰 + 사용자 정보)"""
    token: KakaoTokenResponse = Field(..., description="토큰 정보")
    user_info: KakaoUserInfoResponse = Field(..., description="사용자 정보")
