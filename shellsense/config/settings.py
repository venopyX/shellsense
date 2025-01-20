"""
Configuration settings for ShellSense.

This module provides configuration settings and validation.
"""

import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)


class Config:
    """Configuration settings for ShellSense."""

    # Class-level attributes
    ACCOUNT_ID: Optional[str] = None
    API_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    FUNCTION_CALL_MODEL: str = "@hf/nousresearch/hermes-2-pro-mistral-7b"
    FRIENDLY_RESPONSE_MODEL: str = "@hf/mistral/mistral-7b-instruct-v0.2"
    CLOUDFLARE_API_URL: Optional[str] = None

    @classmethod
    @log_function_call
    def update_from_dict(cls, config: Dict[str, str]) -> None:
        """Update configuration from a dictionary."""
        logger.debug("Updating configuration from dictionary", 
                    extra={"config_keys": list(config.keys())})
        
        cls.OPENAI_API_KEY = config.get("OPENAI_API_KEY")
        cls.GEMINI_API_KEY = config.get("GEMINI_API_KEY")
        cls.ACCOUNT_ID = config.get("CLOUDFLARE_ACCOUNT_ID")
        cls.API_TOKEN = config.get("CLOUDFLARE_AUTH_TOKEN")
        cls.FUNCTION_CALL_MODEL = config.get(
            "FUNCTION_CALL_MODEL", cls.FUNCTION_CALL_MODEL
        )
        cls.FRIENDLY_RESPONSE_MODEL = config.get(
            "FRIENDLY_RESPONSE_MODEL", cls.FRIENDLY_RESPONSE_MODEL
        )
        
        if cls.ACCOUNT_ID and cls.FUNCTION_CALL_MODEL:
            cls.CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/accounts/{cls.ACCOUNT_ID}/ai/run/{cls.FUNCTION_CALL_MODEL}"
            logger.debug("Updated Cloudflare API URL", 
                        extra={"model": cls.FUNCTION_CALL_MODEL})
        
        logger.info("Configuration updated successfully", extra={
            "has_openai": bool(cls.OPENAI_API_KEY),
            "has_gemini": bool(cls.GEMINI_API_KEY),
            "has_cloudflare": bool(cls.ACCOUNT_ID and cls.API_TOKEN),
            "function_call_model": cls.FUNCTION_CALL_MODEL,
            "friendly_response_model": cls.FRIENDLY_RESPONSE_MODEL
        })

    @classmethod
    @log_function_call
    def validate(cls, provider: str = "cloudflare") -> None:
        """
        Validate that all required configuration is present for the specified provider.
        
        Args:
            provider: The AI provider to validate configuration for
        """
        logger.debug("Validating configuration", extra={"provider": provider})
        
        try:
            if provider == "cloudflare":
                if not cls.ACCOUNT_ID:
                    logger.error("Missing Cloudflare account ID")
                    raise ValueError("CLOUDFLARE_ACCOUNT_ID is required for Cloudflare provider")
                if not cls.API_TOKEN:
                    logger.error("Missing Cloudflare auth token")
                    raise ValueError("CLOUDFLARE_AUTH_TOKEN is required for Cloudflare provider")
            elif provider == "openai":
                if not cls.OPENAI_API_KEY:
                    logger.error("Missing OpenAI API key")
                    raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            elif provider == "gemini":
                if not cls.GEMINI_API_KEY:
                    logger.error("Missing Gemini API key")
                    raise ValueError("GEMINI_API_KEY is required for Gemini provider")
            else:
                logger.error("Invalid provider specified", extra={"provider": provider})
                raise ValueError(f"Invalid provider: {provider}")
            
            logger.info("Configuration validation successful", 
                       extra={"provider": provider})
        except ValueError as e:
            logger.error("Configuration validation failed", 
                        extra={"provider": provider, "error": str(e)},
                        exc_info=True)
            raise


@log_function_call
def get_config_file() -> str:
    """Get the path to the config file."""
    config_dir = os.path.expanduser("~/.config/shellsense")
    config_path = os.path.join(config_dir, "config.env")
    logger.debug("Config file path retrieved", extra={"config_path": config_path})
    return config_path


@log_function_call
def load_config() -> Config:
    """Load configuration from the config file."""
    config_file = get_config_file()
    
    if os.path.exists(config_file):
        logger.debug("Loading environment from config file", 
                    extra={"config_file": config_file})
        load_dotenv(config_file)
    else:
        logger.warning("Config file not found", extra={"config_file": config_file})

    Config.update_from_dict(os.environ)
    return Config
