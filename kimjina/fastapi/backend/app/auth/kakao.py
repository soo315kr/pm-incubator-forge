"""Kakao OAuth2 authentication: login redirect and token/user-info handling."""

from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.config import settings

router = APIRouter(prefix="/auth/kakao", tags=["kakao"])


@router.get("/login")
async def kakao_login():
    """Redirect user to Kakao authorization page."""
    if not settings.kakao_client_id or not settings.kakao_redirect_uri:
        raise HTTPException(
            status_code=503,
            detail="Kakao auth not configured (KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI)",
        )
    params = {
        "client_id": settings.kakao_client_id,
        "redirect_uri": settings.kakao_redirect_uri,
        "response_type": "code",
    }
    url = f"{settings.kakao_authorize_url}?{urlencode(params)}"
    return RedirectResponse(url=url)


@router.get("/callback")
async def kakao_callback(code: str | None = None, error: str | None = None):
    """Handle Kakao redirect: exchange code for token and fetch user info."""
    if error:
        raise HTTPException(status_code=400, detail=f"Kakao auth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_res = await client.post(
            settings.kakao_token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": settings.kakao_client_id,
                "client_secret": settings.kakao_client_secret or None,
                "redirect_uri": settings.kakao_redirect_uri,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_res.raise_for_status()
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=502, detail="No access_token in Kakao response")

        # Fetch user info
        user_res = await client.get(
            settings.kakao_user_info_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_res.raise_for_status()
        user_data = user_res.json()

    # Return token + profile (in real app you’d create session/JWT and redirect to frontend)
    return {
        "access_token": access_token,
        "token_type": token_data.get("token_type", "bearer"),
        "expires_in": token_data.get("expires_in"),
        "user": user_data,
    }
