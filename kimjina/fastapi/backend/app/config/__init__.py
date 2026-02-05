"""config 패키지. settings는 load_env() 호출 이후에만 사용해야 한다."""

from app.config.env import load_env

__all__ = ["load_env", "settings"]


def __getattr__(name: str):
    """settings는 lazy import. main에서 load_env() 호출 후 사용되도록 한다."""
    if name == "settings":
        from app.config.settings import get_settings
        s = get_settings()
        # 인스턴스를 패키지에 캐시해, 서브모듈(app.config.settings)이 아닌 Settings 인스턴스가 반환되도록 함
        import sys
        sys.modules[__name__].settings = s
        return s
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
