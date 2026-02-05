"""
환경 변수 로딩 모듈

애플리케이션 시작 시 .env 파일을 로드하여 환경 변수를 초기화합니다.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def load_env() -> None:
    """
    .env 파일을 로드하여 환경 변수를 초기화합니다.
    
    애플리케이션 시작 시 한 번만 호출되어야 합니다.
    """
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)


def get_env(key: str, default: str = None) -> str:
    """
    환경 변수를 가져옵니다.
    
    Args:
        key: 환경 변수 키
        default: 기본값 (환경 변수가 없을 경우, None이면 예외 발생)
        
    Returns:
        환경 변수 값 또는 기본값
        
    Raises:
        ValueError: 환경 변수가 설정되지 않았고 default가 None인 경우
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"환경 변수 {key}가 설정되지 않았습니다.")
    return value
