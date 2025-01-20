"""
Configuration module for ShellSense.

This module handles configuration loading and validation.
"""

import logging
import os
from pathlib import Path
from typing import Dict

from dotenv import dotenv_values, load_dotenv

from .settings import Config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def ensure_config_dir() -> str:
    """
    Ensure the ShellSense config directory exists.

    Returns:
        str: Path to the config directory
    """
    config_dir = os.path.expanduser("~/.config/shellsense")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def create_default_config() -> None:
    """
    Create a default config file if none exists.
    """
    config_dir = ensure_config_dir()
    config_path = os.path.join(config_dir, "config.env")

    if not os.path.exists(config_path):
        default_config = """# ShellSense Configuration
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
CLOUDFLARE_AUTH_TOKEN=your-cloudflare-auth-token
OPENAI_API_KEY=your-openai-api-key  # Optional
GEMINI_API_KEY=your-gemini-api-key  # Optional
FUNCTION_CALL_MODEL=@hf/nousresearch/hermes-2-pro-mistral-7b
FRIENDLY_RESPONSE_MODEL=@hf/mistral/mistral-7b-instruct-v0.2
"""
        with open(config_path, "w") as f:
            f.write(default_config)
        logger.info(f"Created default config at: {config_path}")
    else:
        logger.info(f"Config file already exists at: {config_path}")


def load_config() -> Dict[str, str]:
    """
    Load and validate ShellSense configuration.

    Returns:
        Dict[str, str]: Configuration key-value pairs

    Raises:
        EnvironmentError: If required configuration is missing
    """
    try:
        # Ensure config directory exists
        config_dir = ensure_config_dir()
        config_path = os.path.join(config_dir, "config.env")

        # Create default config if needed
        if not os.path.exists(config_path):
            create_default_config()
            raise EnvironmentError(
                f"Configuration file created at {config_path}. "
                "Please edit it with your API keys."
            )

        # Load config
        logger.info(f"Loading config from: {config_path}")

        # First load the actual values from the file
        env_values = dotenv_values(config_path)
        logger.debug(f"Raw config values: {env_values}")

        # Then load them into environment
        load_dotenv(config_path)

        # Get required values
        required_keys = [
            "CLOUDFLARE_ACCOUNT_ID",
            "CLOUDFLARE_AUTH_TOKEN",
        ]

        config = {}
        missing_keys = []

        for key in required_keys:
            # Try to get from env_values first, then environment
            value = env_values.get(key) or os.getenv(key)
            logger.debug(f"Loading {key}: {value if value else 'Not found'}")
            if not value or value.strip() == "" or value.startswith("your-"):
                missing_keys.append(key)
            else:
                config[key] = value.strip()

        # Get optional values
        optional_keys = [
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
            "FUNCTION_CALL_MODEL",
            "FRIENDLY_RESPONSE_MODEL",
        ]

        for key in optional_keys:
            value = env_values.get(key) or os.getenv(key)
            logger.debug(f"Loading optional {key}: {value if value else 'Not found'}")
            if value and not value.startswith("your-"):
                config[key] = value.strip()

        if missing_keys:
            raise EnvironmentError(
                f"Missing required configuration: {', '.join(missing_keys)}. "
                f"Please edit {config_path} with your API keys."
            )

        logger.info("Configuration loaded successfully")
        return config

    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise


__all__ = ["load_config", "ensure_config_dir", "create_default_config", "Config"]
