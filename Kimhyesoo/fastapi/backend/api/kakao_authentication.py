"""
Kakao 인증 API (컨트롤러 레이어)
"""
from fastapi import APIRouter, HTTPException, Query
from models.kakao_authentication import (
    OAuthLinkResponse,
    AccessTokenResponse,
    TokenWithUserInfoResponse,
)
from services.interfaces.kakao_authentication import KakaoAuthenticationServiceInterface
from services.impl.kakao_authentication import KakaoAuthenticationServiceImpl

_service: KakaoAuthenticationServiceInterface = KakaoAuthenticationServiceImpl()

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])


@router.get("/request-oauth-link", response_model=OAuthLinkResponse)
async def request_oauth_link() -> OAuthLinkResponse:
    try:
        return _service.generate_oauth_link()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인증 URL 생성 중 오류 발생: {str(e)}")


@router.get("/request-access-token-after-redirection", response_model=AccessTokenResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 발급된 인가 코드"),
) -> AccessTokenResponse:
    try:
        return _service.request_access_token(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-user-info", response_model=TokenWithUserInfoResponse)
async def get_user_info_with_token(
    code: str = Query(..., description="Kakao 인증 후 발급된 인가 코드"),
) -> TokenWithUserInfoResponse:
    try:
        token_response = _service.request_access_token(code)
        user_info = _service.get_user_info(token_response.access_token)
        return TokenWithUserInfoResponse(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            refresh_token=token_response.refresh_token,
            expires_in=token_response.expires_in,
            refresh_token_expires_in=token_response.refresh_token_expires_in,
            scope=token_response.scope,
            user_info=user_info,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
