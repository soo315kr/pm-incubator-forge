"""Service implementation for Kakao OAuth."""
from urllib.parse import urlencode
import httpx
from strategy.kakao_authentification.service.kakao_oauth_service import KakaoOAuthServiceInterface
from strategy.kakao_authentification.models.response import OAuthLinkResponse, AccessTokenResponse, KakaoUserInfo
from strategy.config.env import get_env


class KakaoOAuthServiceImpl(KakaoOAuthServiceInterface):
    """Implementation of Kakao OAuth service."""
    
    KAKAO_OAUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    DEFAULT_RESPONSE_TYPE = "code"
    DEFAULT_GRANT_TYPE = "authorization_code"
    
    def __init__(self):
        """Initialize service with environment variables."""
        self._client_id = None
        self._redirect_uri = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from environment variables."""
        try:
            self._client_id = get_env("KAKAO_CLIENT_ID")
            self._redirect_uri = get_env("KAKAO_REDIRECT_URI")
        except ValueError as e:
            raise ValueError(
                f"Failed to load Kakao OAuth configuration: {str(e)}. "
                "Please ensure KAKAO_CLIENT_ID and KAKAO_REDIRECT_URI are set in .env file."
            )
    
    def generate_oauth_url(self) -> OAuthLinkResponse:
        """
        Generate Kakao OAuth authorization URL.
        
        Returns:
            OAuthLinkResponse: Response containing the OAuth URL
            
        Raises:
            ValueError: If required configuration is missing
        """
        if not self._client_id:
            raise ValueError("KAKAO_CLIENT_ID is not set")
        if not self._redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI is not set")
        
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": self.DEFAULT_RESPONSE_TYPE
        }
        
        oauth_url = f"{self.KAKAO_OAUTH_BASE_URL}?{urlencode(params)}"
        
        return OAuthLinkResponse(oauth_url=oauth_url)
    
    def request_access_token(self, code: str) -> AccessTokenResponse:
        """
        Request access token from Kakao using authorization code.
        Also fetches user information using the access token.
        
        Args:
            code: Authorization code received from Kakao OAuth callback
            
        Returns:
            AccessTokenResponse: Response containing access token, user information and related information
            
        Raises:
            ValueError: If required parameters are missing or invalid
            Exception: If token request fails
        """
        if not code:
            raise ValueError("Authorization code is required")
        
        if not self._client_id:
            raise ValueError("KAKAO_CLIENT_ID is not set")
        if not self._redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI is not set")
        
        # Prepare token request data
        data = {
            "grant_type": self.DEFAULT_GRANT_TYPE,
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "code": code
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        
        try:
            # Request token from Kakao
            with httpx.Client() as client:
                response = client.post(
                    self.KAKAO_TOKEN_URL,
                    data=data,
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                token_data = response.json()
            
            access_token = token_data.get("access_token")
            
            # Fetch user information using the access token
            user_info = None
            if access_token:
                try:
                    user_info = self.get_user_info(access_token)
                except Exception as e:
                    # Log error but don't fail the token request
                    # User info fetch failure should not block token issuance
                    pass
            
            # Parse and return token response with user info
            return AccessTokenResponse(
                access_token=access_token,
                token_type=token_data.get("token_type", "bearer"),
                refresh_token=token_data.get("refresh_token"),
                expires_in=token_data.get("expires_in"),
                scope=token_data.get("scope"),
                user_info=user_info
            )
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error_description", error_data.get("error", str(e)))
            except:
                error_detail = str(e)
            raise ValueError(f"Failed to request access token from Kakao: {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Network error while requesting access token: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while requesting access token: {str(e)}")
    
    def get_user_info(self, access_token: str) -> KakaoUserInfo:
        """
        Get Kakao user information using access token.
        
        Args:
            access_token: Kakao access token
            
        Returns:
            KakaoUserInfo: User information
            
        Raises:
            ValueError: If access token is invalid or expired
            Exception: If API request fails
        """
        if not access_token:
            raise ValueError("Access token is required")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        
        try:
            with httpx.Client() as client:
                response = client.get(
                    self.KAKAO_USER_INFO_URL,
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                user_data = response.json()
            
            # Parse Kakao user information
            kakao_account = user_data.get("kakao_account", {})
            properties = user_data.get("properties", {})
            
            return KakaoUserInfo(
                id=user_data.get("id"),
                nickname=properties.get("nickname") or kakao_account.get("profile", {}).get("nickname"),
                email=kakao_account.get("email"),
                profile_image=properties.get("profile_image") or kakao_account.get("profile", {}).get("profile_image_url")
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Access token is invalid or expired")
            error_detail = "Unknown error"
            try:
                error_data = e.response.json()
                error_detail = error_data.get("msg", error_data.get("error_description", str(e)))
            except:
                error_detail = str(e)
            raise ValueError(f"Failed to get user information from Kakao: {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Network error while getting user information: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while getting user information: {str(e)}")
