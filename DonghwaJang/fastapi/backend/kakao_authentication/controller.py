"""카카오 인증 Controller. 요청 받아 서비스 호출 후 응답만 반환 (Service에만 의존)."""
import httpx
from fastapi.responses import HTMLResponse, JSONResponse

from kakao_authentication.service import KakaoAuthService
from kakao_authentication.templates import LOGIN_HTML, ERROR_HTML


def _json_err(status: int, msg: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": msg})


def _from_http_error(e: httpx.HTTPStatusError) -> JSONResponse:
    if e.response is None:
        return _json_err(500, str(e))
    try:
        body = e.response.json()
    except Exception:
        body = {}
    msg = body.get("error_description") or body.get("error") or e.response.text or str(e)
    return _json_err(e.response.status_code, msg)


def login_page(service: KakaoAuthService) -> HTMLResponse:
    try:
        return HTMLResponse(LOGIN_HTML.format(auth_url=service.get_auth_url()))
    except ValueError as e:
        return HTMLResponse(ERROR_HTML.format(msg=e), status_code=500)


def request_oauth_link(service: KakaoAuthService) -> dict | JSONResponse:
    try:
        return service.get_oauth_link_response()
    except ValueError as e:
        return _json_err(400, str(e))


async def request_access_token_after_redirection(code: str, service: KakaoAuthService) -> dict | JSONResponse:
    try:
        return await service.request_access_token_after_redirection(code)
    except ValueError as e:
        return _json_err(400, str(e))
    except httpx.HTTPStatusError as e:
        return _from_http_error(e)
