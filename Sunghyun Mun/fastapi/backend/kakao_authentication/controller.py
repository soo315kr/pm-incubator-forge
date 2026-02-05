"""
Kakao OAuth Controller.
Service Interface에만 의존하며, 구현체를 직접 참조하지 않는다.
요청 전달 및 응답 반환 역할만 수행한다.
"""
import httpx
from fastapi import APIRouter, Depends, HTTPException

from kakao_authentication.schemas import OAuthLinkResponse, TokenResponse
from kakao_authentication.service_interface import KakaoOAuthServiceInterface

router = APIRouter()


def get_kakao_oauth_service() -> KakaoOAuthServiceInterface:
    """DI: Service Interface 구현체를 반환. (구현체는 앱에서 바인딩)"""
    from kakao_authentication.service_impl import KakaoOAuthServiceImpl
    return KakaoOAuthServiceImpl()


@router.get(
    "/request-oauth-link",
    response_model=OAuthLinkResponse,
    summary="Kakao OAuth 인증 URL 발급",
)
def request_oauth_link(
    service: KakaoOAuthServiceInterface = Depends(get_kakao_oauth_service),
) -> OAuthLinkResponse:
    """사용자가 Kakao 인증 요청 시 인증 URL을 생성하여 반환한다."""
    try:
        return service.get_oauth_authorize_url()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/request-access-token-after-redirection",
    response_model=TokenResponse,
    summary="인가 코드로 액세스 토큰 발급 및 사용자 정보 조회",
)
def request_access_token_after_redirection(
    code: str,
    service: KakaoOAuthServiceInterface = Depends(get_kakao_oauth_service),
) -> TokenResponse:
    """인가 코드(code)를 받아 액세스 토큰을 발급하고, 사용자 정보를 함께 반환한다."""
    try:
        return service.request_access_token_after_redirection(code=code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        body = {}
        if e.response:
            try:
                body = e.response.json()
            except Exception:
                body = {}
            msg = body.get("error_description") or body.get("error") or (e.response.text if e.response else "") or str(e)
            status = e.response.status_code
        else:
            msg, status = str(e), 502
        raise HTTPException(status_code=status, detail=msg)
    except Exception:
        raise HTTPException(status_code=502, detail="토큰 발급 중 오류가 발생했습니다.")
