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
    
    애플리케이션 시작 시 한 번만 호출되어야 하며,
    이후 모든 모듈에서 os.getenv() 또는 os.environ을 통해
    환경 변수에 접근할 수 있습니다.
    """
    # 프로젝트 루트 디렉토리 찾기
    current_file = Path(__file__)
    project_root = current_file.parent.parent
    
    # .env 파일 경로
    env_file = project_root / ".env"
    
    # .env 파일이 존재하면 로드
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)
    else:
        # .env 파일이 없어도 경고만 출력하고 계속 진행
        # (환경 변수가 이미 설정되어 있을 수 있음)
        print(f"Warning: .env file not found at {env_file}")
