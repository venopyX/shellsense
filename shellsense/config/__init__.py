"""
Configuration module for ShellSense.

This module handles configuration loading and validation.
"""

import os
from pathlib import Path
from typing import Dict

from dotenv import dotenv_values, load_dotenv

from shellsense.utils.logging_manager import get_logger, log_function_call
from .settings import Config

# Initialize logger for this module
logger = get_logger(__name__)


@log_function_call
def ensure_config_dir() -> str:
    """
    Ensure the ShellSense config directory exists.

    Returns:
        str: Path to the config directory
    """
    config_dir = os.path.expanduser("~/.config/shellsense")
    os.makedirs(config_dir, exist_ok=True)
    logger.debug("Config directory ensured", extra={"config_dir": config_dir})
    return config_dir


@log_function_call
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
        logger.info("Created default config", extra={"config_path": config_path})
    else:
        logger.info("Config file already exists", extra={"config_path": config_path})


@log_function_call
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
            logger.warning("Configuration file not found, created default", 
                         extra={"config_path": config_path})
            raise EnvironmentError(
                f"Configuration file created at {config_path}. "
                "Please edit it with your API keys."
            )

        # Load config
        logger.info("Loading configuration", extra={"config_path": config_path})

        # First load the actual values from the file
        env_values = dotenv_values(config_path)
        logger.debug("Raw config values loaded", 
                    extra={"keys": list(env_values.keys())})

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
            if not value or value.strip() == "" or value.startswith("your-"):
                logger.warning(f"Required key missing or invalid", 
                             extra={"key": key})
                missing_keys.append(key)
            else:
                config[key] = value.strip()
                logger.debug("Required key loaded", 
                           extra={"key": key, "value": "[REDACTED]"})

        # Get optional values
        optional_keys = [
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
            "FUNCTION_CALL_MODEL",
            "FRIENDLY_RESPONSE_MODEL",
        ]

        for key in optional_keys:
            value = env_values.get(key) or os.getenv(key)
            if value and not value.startswith("your-"):
                config[key] = value.strip()
                logger.debug("Optional key loaded", 
                           extra={"key": key, "value": "[REDACTED]" if "API_KEY" in key else value})

        if missing_keys:
            logger.error("Missing required configuration", 
                        extra={"missing_keys": missing_keys})
            raise EnvironmentError(
                f"Missing required configuration: {', '.join(missing_keys)}. "
                f"Please edit {config_path} with your API keys."
            )

        logger.info("Configuration loaded successfully", 
                   extra={"config_keys": list(config.keys())})
        return config

    except Exception as e:
        logger.error("Failed to load configuration", 
                    extra={"error": str(e)}, 
                    exc_info=True)
        raise


__all__ = ["load_config", "ensure_config_dir", "create_default_config", "Config"]
