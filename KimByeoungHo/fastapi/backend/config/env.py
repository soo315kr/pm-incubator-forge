"""
PM-BH-1: 환경 변수 로딩을 위한 config/env 초기화

이 모듈은 애플리케이션 전역에서 사용할 환경 변수를 로드합니다.
python-dotenv를 사용하여 .env 파일을 1회 로드하며,
다른 모듈(Service, Controller)에서는 이 모듈을 통해 환경 변수를 사용합니다.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_env() -> None:
    """
    .env 파일을 로드하여 환경 변수를 설정합니다.
    
    애플리케이션 시작 시 main.py에서 1회 호출되어야 합니다.
    .env 파일이 없어도 예외를 발생시키지 않으며,
    환경 변수가 이미 설정되어 있으면 덮어쓰지 않습니다.
    """
    # backend 디렉토리의 .env 파일 경로
    env_path = Path(__file__).parent.parent / ".env"
    
    # .env 파일 로드 (override=False: 기존 환경 변수 유지)
    load_dotenv(dotenv_path=env_path, override=False)
    
    print(f"[Config] 환경 변수 로드 완료 (path: {env_path})")


def get_env(key: str, default: str = "") -> str:
    """
    환경 변수 값을 가져옵니다.
    
    Args:
        key: 환경 변수 키
        default: 키가 없을 때 반환할 기본값
        
    Returns:
        환경 변수 값 또는 기본값
    """
    return os.getenv(key, default)
