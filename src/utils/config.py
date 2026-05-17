"""
Configuration module for loading environment variables from multiple sources.

Priority order:
1. Runtime environment variables (os.environ)
2. config/.env file
3. config/.env.local file
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class EnvConfig:
    """Manages environment variable loading with fallback strategy."""

    _instance = None
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize and load environment variables if not already loaded."""
        if not EnvConfig._loaded:
            self._load_env_variables()
            EnvConfig._loaded = True

    @staticmethod
    def _load_env_variables():
        """
        Load environment variables with fallback strategy.

        Priority:
        1. Runtime environment variables (already in os.environ)
        2. config/.env
        3. config/.env.local
        """
        # Get the project root (one level up from the src directory)
        project_root = Path(__file__).parent.parent.parent
        config_dir = project_root / "config"

        # Files to try, in order
        env_files = [
            config_dir / ".env",
            config_dir / ".env.local",
        ]

        # Load .env files (only for variables not already in environment)
        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file, override=False)
                print(f"[OK] Loaded environment variables from: {env_file}")
            else:
                print(f"[WARN] Environment file not found: {env_file}")

    @staticmethod
    def get(key: str, default: str = None) -> str:
        """
        Get an environment variable with fallback.

        Args:
            key: Environment variable key
            default: Default value if not found

        Returns:
            Environment variable value or default
        """
        # Ensure environment variables are loaded
        env_config = EnvConfig()
        return os.getenv(key, default)

    @staticmethod
    def get_required(key: str) -> str:
        """
        Get a required environment variable.

        Args:
            key: Environment variable key

        Returns:
            Environment variable value

        Raises:
            ValueError: If the variable is not found
        """
        value = EnvConfig.get(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' not found in runtime, config/.env, or config/.env.local")
        return value


# Create a singleton instance to trigger loading
_env_config = EnvConfig()

