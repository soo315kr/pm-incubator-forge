"""Service implementations. Controllers do not depend on this module directly."""

import httpx
from urllib.parse import urlencode

from config.kakao import (
    KAKAO_AUTHORIZE_URL,
    KAKAO_TOKEN_URL,
    KAKAO_USER_ME_URL,
    get_kakao_client_id,
    get_kakao_client_secret,
    get_kakao_redirect_uri,
)
from kakao_authentication.service_interface import (
    OAuthLinkServiceInterface,
    TokenExchangeServiceInterface,
    UserInfoServiceInterface,
)


def _response_body(resp: httpx.Response):  # noqa: ANN201
    """Parse response body for error messages. Avoids JSONDecodeError when content-type says JSON but body is invalid."""
    if not resp.headers.get("content-type", "").startswith("application/json"):
        return resp.text
    try:
        return resp.json()
    except Exception:
        return resp.text


class OAuthLinkServiceImpl(OAuthLinkServiceInterface):
    """Generates Kakao OAuth authorization URL from env-based config."""

    def get_authorization_url(self) -> str:
        client_id = get_kakao_client_id()
        redirect_uri = get_kakao_redirect_uri()
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        return f"{KAKAO_AUTHORIZE_URL}?{urlencode(params)}"


class TokenExchangeServiceImpl(TokenExchangeServiceInterface):
    """Exchanges authorization code for tokens via Kakao token endpoint."""

    def exchange_code_for_tokens(self, code: str) -> dict:
        if not (code and code.strip()):
            raise ValueError("code is required")
        client_id = get_kakao_client_id()
        redirect_uri = get_kakao_redirect_uri()
        client_secret = get_kakao_client_secret()
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code.strip(),
        }
        if client_secret:
            data["client_secret"] = client_secret
        with httpx.Client() as client:
            resp = client.post(
                KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        if resp.status_code != 200:
            body = _response_body(resp)
            raise ValueError(f"Token exchange failed: {resp.status_code} - {body}")
        return resp.json()


class UserInfoServiceImpl(UserInfoServiceInterface):
    """Fetches Kakao user info using access token."""

    def get_user_info(self, access_token: str) -> dict:
        if not (access_token and access_token.strip()):
            raise ValueError("access_token is required")
        with httpx.Client() as client:
            resp = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token.strip()}"},
            )
        if resp.status_code != 200:
            body = _response_body(resp)
            raise ValueError(f"User info request failed: {resp.status_code} - {body}")
        return resp.json()
