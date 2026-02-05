"""Service interface for Kakao OAuth."""
from abc import ABC, abstractmethod
from strategy.kakao_authentification.models.response import OAuthLinkResponse, AccessTokenResponse, KakaoUserInfo


class KakaoOAuthServiceInterface(ABC):
    """Interface for Kakao OAuth service."""
    
    @abstractmethod
    def generate_oauth_url(self) -> OAuthLinkResponse:
        """
        Generate Kakao OAuth authorization URL.
        
        Returns:
            OAuthLinkResponse: Response containing the OAuth URL
            
        Raises:
            ValueError: If required environment variables are not set
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
