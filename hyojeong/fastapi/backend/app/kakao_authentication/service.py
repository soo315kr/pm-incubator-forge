from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import KakaoUserInfo, TokenResponse


class KakaoAuthenticationService(ABC):
    @abstractmethod
    def build_oauth_link(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def request_access_token(self, code: str) -> TokenResponse:
        raise NotImplementedError

    @abstractmethod
    async def fetch_user_info(self, access_token: str) -> KakaoUserInfo:
        raise NotImplementedError
