"""
환경 변수 로딩 모듈

애플리케이션 시작 시 .env 파일을 로드하여 환경 변수를 초기화합니다.
"""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env(env_file: Optional[str] = None) -> None:
    """
    환경 변수를 로드합니다.
    
    Args:
        env_file: 로드할 .env 파일 경로. None인 경우 프로젝트 루트의 .env 파일을 사용합니다.
    
    Returns:
        None
    """
    if env_file is None:
        # 프로젝트 루트 디렉토리 찾기
        current_dir = Path(__file__).resolve().parent.parent
        env_file = current_dir / ".env"
    
    # .env 파일이 존재하는 경우에만 로드
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        # .env 파일이 없어도 애플리케이션은 실행 가능하도록 경고만 출력
        print(f"Warning: .env file not found at {env_file}")


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    환경 변수 값을 가져옵니다.
    
    Args:
        key: 환경 변수 키
        default: 기본값 (환경 변수가 없을 경우)
    
    Returns:
        환경 변수 값 또는 기본값
    """
    return os.getenv(key, default)


def get_env_required(key: str) -> str:
    """
    필수 환경 변수 값을 가져옵니다.
    환경 변수가 없으면 ValueError를 발생시킵니다.
    
    Args:
        key: 환경 변수 키
    
    Returns:
        환경 변수 값
    
    Raises:
        ValueError: 환경 변수가 설정되지 않은 경우
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value
