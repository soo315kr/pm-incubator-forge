"""Kakao 인증 도메인 DTO."""

from dataclasses import dataclass


@dataclass
class UserInfo:
    """Kakao 사용자 정보. 사용자 ID, 닉네임, 이메일(동의 시) 등."""

    id: int
    nickname: str | None = None
    email: str | None = None
    profile_image_url: str | None = None
    thumbnail_image_url: str | None = None


@dataclass
class TokenResponse:
    """Kakao OAuth 토큰 발급 응답. API 요청에 사용 가능한 액세스 토큰 및 리프레시 토큰 포함."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    refresh_token_expires_in: int
    scope: str | None = None


@dataclass
class TokenWithUserResponse:
    """토큰 발급 결과 + Kakao 사용자 정보. PM-EDDI-3·PM-EDDI-4 통합 반환값."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    refresh_token_expires_in: int
    scope: str | None
    user: UserInfo
