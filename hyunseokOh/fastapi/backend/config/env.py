"""Load .env once at application startup. Do not load .env in services or controllers."""

from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from .env file (once). Safe to call multiple times; dotenv overwrites only if not set."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path, override=False)
