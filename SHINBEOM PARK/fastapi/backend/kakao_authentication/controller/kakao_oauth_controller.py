from fastapi import APIRouter, Depends, HTTPException
from kakao_authentication.service.kakao_oauth_service import KakaoOauthService
from kakao_authentication.service.kakao_oauth_service_impl import KakaoOauthServiceImpl

kakao_oauth_router = APIRouter()

def get_kakao_oauth_service() -> KakaoOauthService:
    return KakaoOauthServiceImpl()

@kakao_oauth_router.get("/kakao-authentication/request-oauth-link")
def request_kakao_oauth_link(service: KakaoOauthService = Depends(get_kakao_oauth_service)):
    try:
        return service.get_kakao_login_link()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@kakao_oauth_router.get("/kakao-authentication/request-access-token-after-redirection")
async def request_access_token(code: str, service: KakaoOauthService = Depends(get_kakao_oauth_service)):
    try:
        return await service.request_access_token(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
