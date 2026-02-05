"""Service implementation for Kakao authentication."""
import httpx
from urllib.parse import urlencode

from config.settings import kakao_oauth_settings
from kakao_authentication.domain.models import (
    AccessTokenRequest,
    AccessTokenResponse,
    AccessTokenWithUserInfoResponse,
    KakaoUserInfo,
    OAuthLinkRequest,
    OAuthLinkResponse,
)
from kakao_authentication.domain.service_interface import (
    KakaoAuthenticationServiceInterface,
)


class KakaoAuthenticationServiceImpl(KakaoAuthenticationServiceInterface):
    """Implementation of Kakao authentication service."""
    
    KAKAO_OAUTH_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    def __init__(self):
        """Initialize service with settings validation."""
        # Ensure environment variables are loaded
        from config.env import load_env
        import os
        from pathlib import Path
        
        # Load env from the correct path
        project_root = Path(__file__).parent.parent.parent
        env_file = project_root / ".env"
        load_env(str(env_file))
        
        # Validate settings
        kakao_oauth_settings.validate()
    
    def generate_oauth_link(self, request: OAuthLinkRequest) -> OAuthLinkResponse:
        """Generate Kakao OAuth authentication URL."""
        params = {
            "client_id": kakao_oauth_settings.client_id,
            "redirect_uri": kakao_oauth_settings.redirect_uri,
            "response_type": "code",
        }
        
        oauth_url = f"{self.KAKAO_OAUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(oauth_url=oauth_url)
    
    def request_access_token(self, request: AccessTokenRequest) -> AccessTokenResponse:
        """Request access token using authorization code."""
        if not request.code:
            raise ValueError("Authorization code is required")
        
        data = {
            "grant_type": "authorization_code",
            "client_id": kakao_oauth_settings.client_id,
            "redirect_uri": kakao_oauth_settings.redirect_uri,
            "code": request.code,
        }
        
        if kakao_oauth_settings.client_secret:
            data["client_secret"] = kakao_oauth_settings.client_secret
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.KAKAO_TOKEN_URL,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data=data,
                )
                response.raise_for_status()
                token_data = response.json()
                
                return AccessTokenResponse(
                    access_token=token_data.get("access_token"),
                    token_type=token_data.get("token_type", "Bearer"),
                    refresh_token=token_data.get("refresh_token"),
                    expires_in=token_data.get("expires_in"),
                    refresh_token_expires_in=token_data.get("refresh_token_expires_in"),
                    scope=token_data.get("scope"),
                )
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json() if e.response else {}
            raise ValueError(
                f"Failed to request access token: {error_detail.get('error_description', str(e))}"
            )
        except Exception as e:
            raise Exception(f"Unexpected error during token request: {str(e)}")
    
    def get_user_info(self, access_token: str) -> dict:
        """Get user information using access token."""
        if not access_token:
            raise ValueError("Access token is required")
        
        try:
            with httpx.Client() as client:
                response = client.get(
                    self.KAKAO_USER_INFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid or expired access token")
            error_detail = e.response.json() if e.response else {}
            raise ValueError(
                f"Failed to get user info: {error_detail.get('error_description', str(e))}"
            )
        except Exception as e:
            raise Exception(f"Unexpected error during user info request: {str(e)}")
    
    def request_access_token_with_user_info(
        self, request: AccessTokenRequest
    ) -> AccessTokenWithUserInfoResponse:
        """Request access token and user information together."""
        # Get access token first
        token_response = self.request_access_token(request)
        
        # Get user info using the access token
        user_info_data = self.get_user_info(token_response.access_token)
        
        # Map user info to domain model
        kakao_account = user_info_data.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        
        user_info = KakaoUserInfo(
            id=user_info_data.get("id"),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
            profile_image=profile.get("profile_image_url"),
        )
        
        return AccessTokenWithUserInfoResponse(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            refresh_token=token_response.refresh_token,
            expires_in=token_response.expires_in,
            refresh_token_expires_in=token_response.refresh_token_expires_in,
            scope=token_response.scope,
            user_info=user_info,
        )
