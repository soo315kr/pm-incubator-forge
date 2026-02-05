from kakao_authentication.service.kakao_oauth_service import KakaoOauthService
from config.env import get_env_config
import httpx

class KakaoOauthServiceImpl(KakaoOauthService):
    def __init__(self):
        self.config = get_env_config()

    def get_kakao_login_link(self) -> dict:
        client_id = self.config.get_kakao_client_id()
        redirect_uri = self.config.get_kakao_redirect_uri()
        
        if not client_id or not redirect_uri:
            raise ValueError("Kakao client_id or redirect_uri is not configured in environment variables.")

        return {
            "auth_url": f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code"
        }

    async def request_access_token(self, code: str) -> dict:
        client_id = self.config.get_kakao_client_id()
        redirect_uri = self.config.get_kakao_redirect_uri()

        if not client_id or not redirect_uri:
             raise ValueError("Kakao client_id or redirect_uri is not configured in environment variables.")

        token_url = "https://kauth.kakao.com/oauth/token"
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code
        }

        async with httpx.AsyncClient() as client:
            try:
                # 1. Request Access Token
                response = await client.post(token_url, headers=headers, data=data)
                response.raise_for_status()
                token_info = response.json()
                access_token = token_info.get("access_token")

                if not access_token:
                     raise ValueError("Failed to retrieve access token from Kakao response.")

                # 2. Get User Info
                user_info = await self.get_user_info(client, access_token)

                return {
                    "token_info": token_info,
                    "user_info": user_info
                }

            except httpx.HTTPStatusError as e:
                raise ValueError(f"Kakao API Error: {e.response.text}")
            except httpx.RequestError as e:
                raise ValueError(f"Network Error during Kakao API request: {str(e)}")

    async def get_user_info(self, client: httpx.AsyncClient, access_token: str) -> dict:
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }

        response = await client.get(user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()
