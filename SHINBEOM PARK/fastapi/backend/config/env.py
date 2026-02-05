import os
from dotenv import load_dotenv

class EnvConfig:
    def __init__(self):
        self.load_env()

    def load_env(self):
        load_dotenv()

    def get_kakao_client_id(self):
        return os.getenv("KAKAO_CLIENT_ID")

    def get_kakao_redirect_uri(self):
        return os.getenv("KAKAO_REDIRECT_URI")

env_config = EnvConfig()

def get_env_config():
    return env_config
