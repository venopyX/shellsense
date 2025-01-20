"""
Provider for generating user-friendly AI responses.

This module provides a FriendlyAiResponse class that transforms raw tool outputs
into user-friendly responses using AI. It uses the Cloudflare API for text
generation and includes error handling and structured logging.

TODO:
- Add response caching for frequently asked queries
- Implement retry mechanism for failed API calls
- Add response validation and sanitization
- Consider adding response templates for common scenarios
- Add metrics collection for response quality
- Add support for different response formats
"""

from typing import Dict, Optional
import requests

from shellsense.ai.prompts import friendly_ai, system_prompt
from shellsense.ai.providers.cloudflare_provider import CloudflareProvider
from shellsense.config.settings import Config
from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)


class FriendlyAiResponse:
    """
    Generates user-friendly responses using Cloudflare's AI API.

    This class handles the transformation of raw tool outputs into user-friendly
    responses using AI. It uses the Cloudflare API for text generation and
    includes error handling and logging.

    Attributes:
        friendly_response_model (str): The AI model to use for response generation
        cloudflare_provider (CloudflareProvider): Provider for AI API calls
    """

    @log_function_call
    def __init__(self):
        """Initialize FriendlyAiResponse with configuration."""
        try:
            Config.validate()  # Validate required config is present
            self.friendly_response_model = Config.FRIENDLY_RESPONSE_MODEL
            self.cloudflare_provider = CloudflareProvider()
            logger.debug("FriendlyAiResponse initialized successfully", extra={
                "model": self.friendly_response_model
            })
        except ValueError as e:
            logger.error("Configuration error in FriendlyAiResponse", extra={
                "error": str(e),
                "error_type": "ValueError"
            })
            raise
        except Exception as e:
            logger.error("Unexpected error during FriendlyAiResponse initialization", extra={
                "error": str(e),
                "error_type": type(e).__name__
            })
            raise

    @log_function_call
    def get_friendly_response(self, user_query: str, tool_output: str) -> str:
        """
        Refines raw tool output into a user-friendly response.

        This method takes the user's original query and tool output, then uses AI
        to generate a more user-friendly and contextual response.

        Args:
            user_query (str): The user's original query.
            tool_output (str): Raw output from tools.

        Returns:
            str: A refined, user-friendly response.

        Raises:
            ValueError: If configuration is invalid or response format is unexpected
            requests.exceptions.RequestException: If the API request fails
            Exception: For any other unexpected errors
        """
        if not user_query or not tool_output:
            logger.error("Invalid input: empty parameters", extra={
                "has_user_query": bool(user_query),
                "has_tool_output": bool(tool_output)
            })
            raise ValueError("User query and tool output are required")

        try:
            # Prepare messages for the AI
            messages = [
                {"role": "system", "content": system_prompt()},
                {"role": "system", "content": friendly_ai()},
                {"role": "user", "content": f"Original Question: {user_query}\n\nTool Output:\n{tool_output}"}
            ]

            logger.debug("Sending request to AI provider", extra={
                "model": self.friendly_response_model,
                "message_count": len(messages),
                "query_length": len(user_query),
                "output_length": len(tool_output)
            })
            
            # Get response from Cloudflare
            response = self.cloudflare_provider.chat(
                messages=messages,
                model=self.friendly_response_model
            )

            logger.debug("Received response from Cloudflare", extra={
                "response_type": type(response).__name__,
                "response_length": len(str(response))
            })

            # Extract response content
            if not response:
                logger.error("Empty response from Cloudflare API")
                return "I apologize, but I couldn't generate a proper response at this time. Please try again."

            # Handle different response formats
            if isinstance(response, dict):
                # New format: {"result": {"response": "..."}}
                result = response.get("result", {}).get("response", "")
                logger.debug("Processing dictionary response", extra={
                    "has_result": "result" in response,
                    "has_response": "response" in response.get("result", {})
                })
            elif isinstance(response, str):
                # Direct string response
                result = response
                logger.debug("Processing string response", extra={
                    "response_length": len(response)
                })
            else:
                logger.error("Unexpected response type from Cloudflare", extra={
                    "response_type": type(response).__name__
                })
                return "I apologize, but I received an unexpected response format. Please try again."

            # Validate and return result
            if not result or not isinstance(result, str):
                logger.warning("No valid response content generated", extra={
                    "result_type": type(result).__name__,
                    "is_empty": not bool(result)
                })
                return "I apologize, but I couldn't generate a proper response at this time. Please try again."

            logger.info("Successfully generated friendly response", extra={
                "response_length": len(result),
                "contains_apology": "apologize" in result.lower()
            })
            return result.strip()

        except requests.exceptions.RequestException as e:
            logger.error("API request failed", extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "model": self.friendly_response_model
            })
            raise
        except Exception as e:
            logger.error("Unexpected error in get_friendly_response", extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "model": self.friendly_response_model
            })
            raise
