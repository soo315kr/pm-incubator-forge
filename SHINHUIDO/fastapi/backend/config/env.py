"""
환경 변수 로딩 모듈

애플리케이션 시작 시 .env 파일을 로드하여 환경 변수를 초기화합니다.
이 모듈은 애플리케이션 전역에서 환경 변수 로딩을 일관되게 보장합니다.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_env() -> None:
    """
    .env 파일을 로드하여 환경 변수를 초기화합니다.
    
    애플리케이션 시작 시 한 번만 호출되어야 하며,
    이후 모든 모듈에서 os.getenv() 또는 os.environ을 통해
    환경 변수에 접근할 수 있습니다.
    """
    # 프로젝트 루트 디렉토리 찾기 (backend 디렉토리)
    backend_dir = Path(__file__).parent.parent
    env_file = backend_dir / ".env"
    
    # .env 파일이 존재하는 경우에만 로드
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)
    else:
        # .env 파일이 없어도 환경 변수는 시스템 환경 변수에서 로드 가능
        load_dotenv(override=False)

