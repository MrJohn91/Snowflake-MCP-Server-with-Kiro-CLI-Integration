"""Configuration management for Snowflake MCP Server."""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Required Snowflake connection parameters
SNOWFLAKE_ACCOUNT: Optional[str] = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER: Optional[str] = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD: Optional[str] = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE: Optional[str] = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE: Optional[str] = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA: Optional[str] = os.getenv("SNOWFLAKE_SCHEMA", "GOLD")
SNOWFLAKE_ROLE: Optional[str] = os.getenv("SNOWFLAKE_ROLE")

# Optional connection settings
SNOWFLAKE_TIMEOUT: int = int(os.getenv("SNOWFLAKE_TIMEOUT", "30"))
SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE: bool = (
    os.getenv("SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE", "true").lower() == "true"
)
SNOWFLAKE_AUTHENTICATOR: str = os.getenv("SNOWFLAKE_AUTHENTICATOR", "snowflake")

# Connection retry settings
MAX_CON_RETRY_ATTEMPTS: int = int(os.getenv("MAX_CON_RETRY_ATTEMPTS", "3"))
SNOWFLAKE_LOGIN_TIMEOUT: int = int(os.getenv("SNOWFLAKE_LOGIN_TIMEOUT", "120"))

# Flask configuration
FLASK_HOST: str = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT: int = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"



MOCK_MODE = False

def validate_config() -> None:
    """Validate that all required configuration is present."""
    global MOCK_MODE
    
    # Allow forcing mock mode via environment variable (for testing)
    if os.getenv("FORCE_MOCK_MODE", "").lower() == "true":
        import logging
        logging.getLogger(__name__).info("FORCE_MOCK_MODE enabled - using simulated data")
        MOCK_MODE = True
        return
    
    required_vars = [
        ("SNOWFLAKE_ACCOUNT", SNOWFLAKE_ACCOUNT),
        ("SNOWFLAKE_USER", SNOWFLAKE_USER),
        ("SNOWFLAKE_WAREHOUSE", SNOWFLAKE_WAREHOUSE),
        ("SNOWFLAKE_DATABASE", SNOWFLAKE_DATABASE),
        ("SNOWFLAKE_ROLE", SNOWFLAKE_ROLE),
    ]
    
    # Password is only required if not using external browser auth
    if SNOWFLAKE_AUTHENTICATOR != "externalbrowser":
        required_vars.append(("SNOWFLAKE_PASSWORD", SNOWFLAKE_PASSWORD))

    missing_vars = [name for name, value in required_vars if not value]

    if missing_vars:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Server will run in MOCK MODE (Simulated Data)."
        )
        MOCK_MODE = True
        return

    MOCK_MODE = False


def get_snowflake_config() -> dict:
    """Get Snowflake connection configuration as a dictionary."""
    validate_config()
    
    if MOCK_MODE:
        return {}

    config = {
        "account": SNOWFLAKE_ACCOUNT,
        "user": SNOWFLAKE_USER,
        "warehouse": SNOWFLAKE_WAREHOUSE,
        "database": SNOWFLAKE_DATABASE,
        "schema": SNOWFLAKE_SCHEMA,
        "role": SNOWFLAKE_ROLE,
        "authenticator": SNOWFLAKE_AUTHENTICATOR,
        "client_session_keep_alive": SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE,
        "network_timeout": SNOWFLAKE_TIMEOUT,
        "login_timeout": SNOWFLAKE_LOGIN_TIMEOUT,
    }
    
    # Only add password if not using external browser auth
    if SNOWFLAKE_AUTHENTICATOR != "externalbrowser" and SNOWFLAKE_PASSWORD:
        config["password"] = SNOWFLAKE_PASSWORD
        
    return config
