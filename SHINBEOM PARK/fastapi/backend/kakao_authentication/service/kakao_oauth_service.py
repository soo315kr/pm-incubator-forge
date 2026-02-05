from abc import ABC, abstractmethod

class KakaoOauthService(ABC):
    @abstractmethod
    def get_kakao_login_link(self) -> dict:
        pass

    @abstractmethod
    async def request_access_token(self, code: str) -> dict:
        pass
