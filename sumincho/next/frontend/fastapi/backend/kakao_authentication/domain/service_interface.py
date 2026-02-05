"""Service interface for Kakao authentication."""
from abc import ABC, abstractmethod

from kakao_authentication.domain.models import (
    AccessTokenRequest,
    AccessTokenResponse,
    AccessTokenWithUserInfoResponse,
    OAuthLinkRequest,
    OAuthLinkResponse,
)


class KakaoAuthenticationServiceInterface(ABC):
    """Interface for Kakao authentication service."""
    
    @abstractmethod
    def generate_oauth_link(self, request: OAuthLinkRequest) -> OAuthLinkResponse:
        """
        Generate Kakao OAuth authentication URL.
        
        Args:
            request: OAuth link request
            
        Returns:
            OAuth link response containing the authentication URL
            
        Raises:
            ValueError: If required configuration is missing
        """
        pass
    
    @abstractmethod
    def request_access_token(self, request: AccessTokenRequest) -> AccessTokenResponse:
        """
        Request access token using authorization code.
        
        Args:
            request: Access token request containing authorization code
            
        Returns:
            Access token response containing token information
            
        Raises:
            ValueError: If authorization code is invalid or missing
            Exception: If token request fails
        """
        pass
    
    @abstractmethod
    def get_user_info(self, access_token: str) -> dict:
        """
        Get user information using access token.
        
        Args:
            access_token: Kakao access token
            
        Returns:
            User information dictionary
            
        Raises:
            ValueError: If access token is invalid
            Exception: If API request fails
        """
        pass
    
    @abstractmethod
    def request_access_token_with_user_info(
        self, request: AccessTokenRequest
    ) -> AccessTokenWithUserInfoResponse:
        """
        Request access token and user information together.
        
        Args:
            request: Access token request containing authorization code
            
        Returns:
            Access token response with user information
            
        Raises:
            ValueError: If authorization code is invalid or missing
            Exception: If token or user info request fails
        """
        pass
