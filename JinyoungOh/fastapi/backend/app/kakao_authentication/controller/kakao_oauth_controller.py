"""
Kakao OAuth Controller.
요청 전달 및 응답 반환만 수행하며, Service Interface에만 의존한다.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.kakao_authentication.exceptions import (
    KakaoOAuthConfigError,
    KakaoOAuthTokenError,
    KakaoUserInfoError,
)
from app.kakao_authentication.service.kakao_oauth_service import KakaoOAuthService

security = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])


class OAuthLinkResponse(BaseModel):
    """Kakao OAuth 인증 URL 생성 API 응답 (PM-EDDI-2)."""

    url: str


class AccessTokenUserInfoResponse(BaseModel):
    """액세스 토큰 발급 시 함께 반환되는 사용자 정보 (PM-EDDI-4 연동)."""

    id: int
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile_image_url: Optional[str] = None
    thumbnail_image_url: Optional[str] = None


class AccessTokenResponse(BaseModel):
    """인가 코드 교환 API 응답 (PM-EDDI-3). 액세스 토큰·리프레시 토큰·만료 시간·사용자 정보."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    user_info: Optional[AccessTokenUserInfoResponse] = None


def get_kakao_oauth_service() -> KakaoOAuthService:
    """Service Interface를 반환하는 의존성. 구현체는 여기서만 주입된다."""
    from app.kakao_authentication.service.kakao_oauth_service_impl import (
        KakaoOAuthServiceImpl,
    )
    return KakaoOAuthServiceImpl()


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    responses={
        200: {"description": "Kakao OAuth 인증 URL 생성 성공. url로 인증 페이지 이동 가능."},
        503: {"description": "필수 환경 변수(client_id, redirect_uri) 누락 등 설정 오류."},
    },
)
def request_oauth_link(
    service: KakaoOAuthService = Depends(get_kakao_oauth_service),
) -> OAuthLinkResponse:
    """
    Kakao OAuth 인증 URL을 생성하여 반환한다.
    client_id, redirect_uri, response_type 등 필수 파라미터는 서버 환경 변수에서 로드된다.
    사용자는 반환된 url로 Kakao 인증 페이지로 즉시 이동할 수 있다.
    """
    try:
        url = service.get_oauth_link()
        return OAuthLinkResponse(url=url)
    except KakaoOAuthConfigError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Kakao OAuth 설정이 올바르지 않습니다.",
                "detail": e.message,
            },
        )


@router.get(
    "/request-access-token-after-redirection",
    response_model=AccessTokenResponse,
    responses={
        200: {"description": "액세스 토큰·리프레시 토큰 발급 성공. access_token으로 Kakao API 요청 가능, expires_in(초) 만료."},
        400: {"description": "잘못된 인가 코드 또는 Kakao 토큰 서버 오류."},
        502: {"description": "토큰 발급 후 사용자 정보 조회 실패 (토큰은 정상 발급됨)."},
        503: {"description": "필수 환경 변수(client_id, redirect_uri) 누락 등 설정 오류."},
        422: {"description": "필수 쿼리 파라미터 code 누락."},
    },
)
def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 리다이렉트로 받은 인가 코드 (필수)"),
    service: KakaoOAuthService = Depends(get_kakao_oauth_service),
) -> AccessTokenResponse:
    """
    인가 코드(code)를 받아 Kakao 액세스 토큰을 발급받고, 사용자 정보를 조회해 함께 반환한다 (PM-EDDI-3).
    client_id, redirect_uri, grant_type은 서버 환경 변수에서 로드된다.
    발급된 액세스 토큰은 바로 Kakao API 요청에 사용 가능하며, 만료 시간(expires_in) 및 리프레시 토큰을 포함한다.
    잘못된 코드 또는 code 누락 시 적절한 오류 메시지를 반환한다.
    """
    try:
        token = service.exchange_code_for_token(code)
        user_info_resp = None
        if token.user_info is not None:
            user_info_resp = AccessTokenUserInfoResponse(
                id=token.user_info.id,
                nickname=token.user_info.nickname,
                email=token.user_info.email,
                profile_image_url=token.user_info.profile_image_url,
                thumbnail_image_url=token.user_info.thumbnail_image_url,
            )
        return AccessTokenResponse(
            access_token=token.access_token,
            token_type=token.token_type,
            refresh_token=token.refresh_token,
            expires_in=token.expires_in,
            refresh_token_expires_in=token.refresh_token_expires_in,
            scope=token.scope,
            user_info=user_info_resp,
        )
    except KakaoOAuthConfigError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Kakao OAuth 설정이 올바르지 않습니다.",
                "detail": e.message,
            },
        )
    except KakaoOAuthTokenError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "액세스 토큰 발급에 실패했습니다.",
                "detail": e.message,
            },
        )
    except KakaoUserInfoError as e:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "토큰 발급 후 사용자 정보 조회에 실패했습니다.",
                "detail": e.message,
            },
        )


@router.get(
    "/user-info",
    response_model=AccessTokenUserInfoResponse,
    responses={
        200: {"description": "Kakao 사용자 정보 조회 성공. id, 닉네임, 이메일(동의 시) 등 반환 (PM-EDDI-4)."},
        401: {"description": "액세스 토큰 없음, 또는 토큰이 유효하지 않거나 만료됨. 적절한 오류 메시지 반환."},
    },
)
def get_user_info(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    access_token: Optional[str] = Query(None, description="Kakao 액세스 토큰 (Bearer 대신 쿼리로 전달 가능)"),
    service: KakaoOAuthService = Depends(get_kakao_oauth_service),
) -> AccessTokenUserInfoResponse:
    """
    PM-EDDI-3에서 발급받은 액세스 토큰으로 Kakao 사용자 정보를 조회한다 (PM-EDDI-4).
    조회 가능한 정보: 사용자 ID(id), 닉네임(nickname), 이메일(동의 시 email), 프로필 이미지 URL 등.
    액세스 토큰이 유효하지 않거나 만료된 경우 401과 함께 적절한 오류 메시지를 반환한다.
    Authorization: Bearer <token> 또는 쿼리 파라미터 access_token으로 토큰을 전달한다.
    """
    token = None
    if credentials:
        token = credentials.credentials
    if not token and access_token:
        token = access_token
    if not token:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "액세스 토큰이 필요합니다.",
                "detail": "Authorization: Bearer <token> 헤더 또는 access_token 쿼리 파라미터를 사용하세요.",
            },
        )

    try:
        user_info = service.get_user_info(token)
        return AccessTokenUserInfoResponse(
            id=user_info.id,
            nickname=user_info.nickname,
            email=user_info.email,
            profile_image_url=user_info.profile_image_url,
            thumbnail_image_url=user_info.thumbnail_image_url,
        )
    except KakaoUserInfoError as e:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "사용자 정보를 조회할 수 없습니다.",
                "detail": e.message,
            },
        )
