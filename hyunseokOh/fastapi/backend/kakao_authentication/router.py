"""FastAPI router: wires implementations and delegates to controller."""

from fastapi import APIRouter, Depends, Header, Query

from kakao_authentication.controller import (
    get_oauth_link,
    get_user_info,
    request_access_token_after_redirection,
)
from kakao_authentication.service_interface import (
    OAuthLinkServiceInterface,
    TokenExchangeServiceInterface,
    UserInfoServiceInterface,
)
from kakao_authentication.service_impl import (
    OAuthLinkServiceImpl,
    TokenExchangeServiceImpl,
    UserInfoServiceImpl,
)

router = APIRouter()


def _oauth_link_service() -> OAuthLinkServiceInterface:
    return OAuthLinkServiceImpl()


def _token_service() -> TokenExchangeServiceInterface:
    return TokenExchangeServiceImpl()


def _user_info_service() -> UserInfoServiceInterface:
    return UserInfoServiceImpl()


@router.get("/request-oauth-link")
def request_oauth_link_endpoint(
    service: OAuthLinkServiceInterface = Depends(_oauth_link_service),
):
    """Return Kakao OAuth authorization URL."""
    return get_oauth_link(service=service)


@router.get("/request-access-token-after-redirection")
def request_access_token_after_redirection_endpoint(
    code: str | None = Query(None),
    token_service: TokenExchangeServiceInterface = Depends(_token_service),
    user_info_service: UserInfoServiceInterface = Depends(_user_info_service),
):
    """Exchange authorization code for access_token (and user info)."""
    return request_access_token_after_redirection(
        code=code,
        service=token_service,
        user_info_service=user_info_service,
    )


@router.get("/user-info")
def user_info_endpoint(
    access_token: str | None = Query(None, alias="access_token"),
    authorization: str | None = Header(None),
    service: UserInfoServiceInterface = Depends(_user_info_service),
):
    """Return Kakao user info. Token via ?access_token=... or Authorization: Bearer <token>."""
    token = access_token
    if not token and authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
    return get_user_info(access_token=token, service=service)
