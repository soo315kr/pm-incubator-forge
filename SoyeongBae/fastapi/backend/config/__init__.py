"""config 패키지: 환경 변수 로딩 등 애플리케이션 설정 책임."""

from config.env import load_env

__all__ = ["load_env"]
