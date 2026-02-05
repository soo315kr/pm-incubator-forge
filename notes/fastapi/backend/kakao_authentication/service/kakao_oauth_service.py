import os
from urllib.parse import urlencode
from typing import Optional
from fastapi import HTTPException


class KakaoOAuthService:
    """Kakao OAuth 인증 서비스"""
    
    KAKAO_AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
    
    def __init__(self):
        """서비스 초기화"""
        # 환경변수에서 기본 클라이언트 ID 가져오기
        self.default_client_id = os.getenv("KAKAO_CLIENT_ID")
    
    def generate_auth_url(
        self,
        redirect_uri: str,
        client_id: Optional[str] = None,
        response_type: str = "code"
    ) -> str:
        """
        Kakao 인증 URL 생성
        
        Args:
            redirect_uri: 리다이렉트 URI
            client_id: Kakao 앱 REST API 키 (없으면 환경변수에서 가져옴)
            response_type: 응답 타입 (기본값: "code")
        
        Returns:
            생성된 Kakao 인증 URL
        
        Raises:
            HTTPException: 필수 파라미터가 없을 경우
        """
        # client_id 검증
        if not client_id:
            if not self.default_client_id:
                raise HTTPException(
                    status_code=400,
                    detail="client_id가 제공되지 않았고 환경변수 KAKAO_CLIENT_ID도 설정되지 않았습니다."
                )
            client_id = self.default_client_id
        
        # response_type 검증
        if response_type not in ["code"]:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 response_type입니다: {response_type}"
            )
        
        # URL 파라미터 구성
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type
        }
        
        # 인증 URL 생성
        auth_url = f"{self.KAKAO_AUTH_BASE_URL}?{urlencode(params)}"
        
        return auth_url
