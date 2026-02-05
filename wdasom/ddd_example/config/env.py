import os
from dotenv import load_dotenv

def load_fastapi_env(env_path: str = ".env") -> None:
    """
    .env 파일을 1회 로드하고, 애플리케이션 전역에서 os.getenv 사용 가능하도록 설정
    """
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"{env_path} 파일을 찾을 수 없습니다.")

    load_dotenv(dotenv_path=env_path)
