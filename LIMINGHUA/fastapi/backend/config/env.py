"""
Environment variable loading. Called once at application startup.
Service and Controller must not load .env directly; use os.getenv after load_env has run.
"""
from pathlib import Path

from dotenv import load_dotenv

_env_loaded = False


def load_env(env_file: str | None = ".env") -> None:
    """Load .env once. Idempotent; repeated calls do not re-load."""
    global _env_loaded
    if _env_loaded:
        return
    if env_file:
        # Use path relative to backend root so .env is found regardless of cwd
        backend_root = Path(__file__).resolve().parent.parent
        path = backend_root / env_file
    else:
        path = None
    load_dotenv(dotenv_path=path)
    _env_loaded = True
