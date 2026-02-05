"""Environment variable loading module."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env(env_file: Optional[str] = None) -> None:
    """
    Load environment variables from .env file.
    
    This function should be called once at application startup.
    If env_file is not provided, it will look for .env in the project root.
    
    Args:
        env_file: Optional path to .env file. If None, searches for .env in project root.
    """
    if env_file is None:
        # Find project root (where this file is located, go up to backend directory)
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
    
    # Use override=True to ensure .env values take precedence
    load_dotenv(dotenv_path=env_file, override=True)
