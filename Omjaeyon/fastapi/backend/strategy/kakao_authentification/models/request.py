"""Request models for Kakao authentication."""
from pydantic import BaseModel, Field


class AccessTokenRequest(BaseModel):
    """Request model for access token generation."""
    code: str = Field(..., description="Authorization code received from Kakao OAuth")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "authorization_code_from_kakao"
            }
        }
