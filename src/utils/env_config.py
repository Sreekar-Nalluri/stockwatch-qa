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
        # src/utils/env_config.py  →  src/utils  →  src  →  project root
        project_root = Path(__file__).parent.parent.parent
        config_dir = project_root / "config"

        for env_file in [config_dir / ".env", config_dir / ".env.local"]:
            if env_file.exists():
                load_dotenv(env_file, override=False)
                print(f"[OK]   Loaded env from: {env_file}")
            else:
                print(f"[WARN] Env file not found: {env_file}")

    # ------------------------------------------------------------------
    # Generic accessors
    # ------------------------------------------------------------------

    @staticmethod
    def get(key: str, default: str = None) -> str:
        """
        Return an environment variable, loading .env files first if needed.

        Args:
            key:     Environment variable name.
            default: Fallback value when the key is absent.

        Returns:
            The variable's value, or *default*.
        """
        EnvConfig()           # ensure singleton / loading has run
        return os.getenv(key, default)

    @staticmethod
    def get_required(key: str) -> str:
        """
        Return a required environment variable, raising if absent.

        Args:
            key: Environment variable name.

        Returns:
            The variable's value.

        Raises:
            ValueError: When the variable is not set in any source.
        """
        value = EnvConfig.get(key)
        if not value:
            raise ValueError(
                f"Required env var '{key}' not found in runtime env, "
                "config/.env, or config/.env.local"
            )
        return value

    @staticmethod
    def finnhub_key() -> str:
        """
        Return the Finnhub API key (FINNHUB_KEY).

        Raises:
            ValueError: When FINNHUB_KEY is not configured.

        Example::

            from utils.config import EnvConfig
            client = finnhub.Client(api_key=EnvConfig.finnhub_key())
        """
        return EnvConfig.get_required("FINNHUB_KEY")

    @staticmethod
    def base_url(default: str = "http://localhost:8080/dashboard.html") -> str:
        return EnvConfig.get("BASE_URL", default)

    @staticmethod
    def symbol(default: str = "AAPL") -> str:
        return EnvConfig.get("SYMBOL", default)

    @staticmethod
    def browser_type(default: str = "chromium") -> str:
        return EnvConfig.get("BROWSER_TYPE", default)

    @staticmethod
    def headless(default: bool = True) -> bool:
        raw = EnvConfig.get("HEADLESS", str(default))
        return raw.strip().lower() == "true"

    @staticmethod
    def server_port(default: int = 8080) -> int:
        raw = EnvConfig.get("SERVER_PORT", str(default))
        try:
            return int(raw)
        except ValueError:
            return default


# Trigger loading on import
_env_config = EnvConfig()