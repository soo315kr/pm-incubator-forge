"""Environment variable loading module."""
from dotenv import load_dotenv
import os
from pathlib import Path


def load_env() -> None:
    """
    Load environment variables from .env file.
    
    This function should be called once at application startup.
    The .env file should be located in the project root directory.
    """
    # Get the project root directory (backend directory)
    backend_dir = Path(__file__).parent.parent.parent
    env_file = backend_dir / ".env"
    env_file_upper = backend_dir / ".ENV"

    # Load .env file if it exists (.env or .ENV for Windows compatibility)
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)
    elif env_file_upper.exists():
        load_dotenv(dotenv_path=env_file_upper, override=False)
    else:
        # If .env doesn't exist, try loading from current directory
        load_dotenv(override=False)


def get_env(key: str, default: str = None) -> str:
    """
    Get environment variable value.
    
    Args:
        key: Environment variable key
        default: Default value if key is not found
        
    Returns:
        Environment variable value or default value
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable '{key}' is not set and no default value provided")
    return value
