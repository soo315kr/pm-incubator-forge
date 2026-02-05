"""Kakao 인증 도메인 (PM-EDDI-2, PM-EDDI-3, PM-EDDI-4)."""

from app.kakao_authentication.controller import router as kakao_authentication_router

__all__ = ["kakao_authentication_router"]
