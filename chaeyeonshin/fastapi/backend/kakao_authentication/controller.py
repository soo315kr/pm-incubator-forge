"""Kakao 인증 Controller. Service Interface에만 의존하며 요청 전달 및 응답 반환만 수행한다."""
import html
import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from kakao_authentication.schemas import OAuthLinkResponse, TokenAndUserResponse
from kakao_authentication.service_interface import KakaoAuthServiceInterface


def get_router(service: KakaoAuthServiceInterface) -> APIRouter:
    """Service Interface를 주입받아 라우터를 반환한다. 구현체는 호출부(main)에서 주입."""
    svc = service
    router = APIRouter()

    @router.get(
        "/request-oauth-link",
        response_class=HTMLResponse,
        summary="Kakao OAuth 인증 URL 생성 (클릭 가능한 링크)",
    )
    def request_oauth_link() -> HTMLResponse:
        try:
            result = svc.get_oauth_link()
            url = html.escape(result.url)
            body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>카카오 로그인</title></head>
<body>
  <p><a href="{url}">카카오 로그인</a></p>
</body>
</html>"""
            return HTMLResponse(content=body)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get(
        "/request-access-token-after-redirection",
        response_model=TokenAndUserResponse,
        summary="인가 코드로 액세스 토큰 발급 및 사용자 정보 조회",
    )
    def request_access_token_after_redirection(
        code: str = Query(..., description="Kakao 인증 후 리다이렉트된 인가 코드"),
    ) -> TokenAndUserResponse:
        try:
            return svc.exchange_code_for_token_and_user(code=code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text or "Kakao API 요청 실패",
            )

    return router
