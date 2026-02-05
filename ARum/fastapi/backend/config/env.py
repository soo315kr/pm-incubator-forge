"""환경 변수 로딩. 애플리케이션 시작 시 1회 호출한다."""

from pathlib import Path

from dotenv import load_dotenv


def load_env(env_file: str | Path = ".env") -> None:
    """
    .env 파일을 로드하여 환경 변수로 주입한다.
    프로젝트 루트 기준 경로를 사용하며, 파일이 없어도 예외를 발생시키지 않는다.
    """
    path = Path(env_file)
    if not path.is_absolute():
        # 실행 위치가 backend가 아닐 수 있으므로, 이 파일 기준 상위 디렉터리에서 .env 탐색
        base = Path(__file__).resolve().parent.parent
        path = base / env_file
    load_dotenv(path, override=False)
