"""Controllers: request/response only. Depend on service interfaces only."""

from fastapi import HTTPException

from kakao_authentication.service_interface import (
    OAuthLinkServiceInterface,
    TokenExchangeServiceInterface,
    UserInfoServiceInterface,
)

def get_oauth_link(service: OAuthLinkServiceInterface) -> dict:
    try:
        url = service.get_authorization_url()
        return {
            "auth url": url
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def request_access_token_after_redirection(
    code: str | None,
    service: TokenExchangeServiceInterface,
    user_info_service: UserInfoServiceInterface,
) -> dict:
    if not code:
        raise HTTPException(status_code=400, detail="code is required")
    try:
        tokens = service.exchange_code_for_tokens(code)
        access_token = tokens.get("access_token")
        if access_token:
            try:
                user_info = user_info_service.get_user_info(access_token)
                tokens["user"] = user_info
            except Exception as e:
                tokens["user_info_error"] = str(e)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_user_info(access_token: str | None, service: UserInfoServiceInterface) -> dict:
    if not access_token:
        raise HTTPException(status_code=401, detail="access_token is required")
    try:
        return service.get_user_info(access_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
