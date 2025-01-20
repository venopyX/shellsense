"""
Provider for generating user-friendly AI responses.

TODO:
- Add response caching for frequently asked queries
- Implement retry mechanism for failed API calls
- Add response validation and sanitization
- Consider adding response templates for common scenarios
- Add metrics collection for response quality
"""

import logging
from typing import Dict, Optional

import requests

from shellsense.ai.prompts import friendly_ai, system_prompt
from shellsense.ai.providers.cloudflare_provider import CloudflareProvider
from shellsense.config.settings import Config

logger = logging.getLogger(__name__)


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

    def __init__(self):
        """Initialize FriendlyAiResponse with configuration."""
        try:
            Config.validate()  # Validate required config is present
            self.friendly_response_model = Config.FRIENDLY_RESPONSE_MODEL
            self.cloudflare_provider = CloudflareProvider()
            logger.debug("FriendlyAiResponse initialized successfully")
        except ValueError as e:
            logger.error(f"Configuration error in FriendlyAiResponse: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error during FriendlyAiResponse initialization: {e}"
            )
            raise

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
            logger.error("Invalid input: user_query and tool_output must not be empty")
            raise ValueError("User query and tool output are required")

        try:
            # Prepare messages for the AI
            messages = [
                {"role": "system", "content": system_prompt()},
                {"role": "system", "content": friendly_ai()},
                {"role": "user", "content": f"Original Question: {user_query}\n\nTool Output:\n{tool_output}"}
            ]

            logger.debug(
                f"Sending request to AI provider with model: {self.friendly_response_model}"
            )
            
            # Get response from Cloudflare
            response = self.cloudflare_provider.chat(
                messages=messages,
                model=self.friendly_response_model
            )

            logger.debug(f"Raw response from Cloudflare: {response}")

            # Extract response content
            if not response:
                logger.error("Empty response from Cloudflare API")
                return "I apologize, but I couldn't generate a proper response at this time. Please try again."

            # Handle different response formats
            if isinstance(response, dict):
                # New format: {"result": {"response": "..."}}
                result = response.get("result", {}).get("response", "")
            elif isinstance(response, str):
                # Direct string response
                result = response
            else:
                logger.error(f"Unexpected response type from Cloudflare: {type(response)}")
                return "I apologize, but I received an unexpected response format. Please try again."

            # Validate and return result
            if not result or not isinstance(result, str):
                logger.warning("No valid response content generated from AI")
                return "I apologize, but I couldn't generate a proper response at this time. Please try again."

            logger.debug("Successfully generated friendly response")
            return result.strip()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_friendly_response: {str(e)}")
            raise
