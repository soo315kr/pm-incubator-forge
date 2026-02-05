from __future__ import annotations

import os
from typing import Final

from dotenv import load_dotenv

_LOADED: bool = False
_ENV_PATH: Final[str] = ".env"


def load_env() -> bool:
    """Load environment variables once at startup."""
    global _LOADED
    if _LOADED:
        return False

    load_dotenv(_ENV_PATH)
    _LOADED = True
    return True


def get_env(name: str, default: str | None = None) -> str | None:
    """Fetch an environment variable without direct dotenv usage elsewhere."""
    return os.getenv(name, default)
