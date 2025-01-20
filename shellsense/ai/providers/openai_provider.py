"""
Manages API interactions with OpenAI.

This module provides an OpenAIProvider class that handles all interactions with
OpenAI's GPT models, including tool calling functionality.

TODO:
- Add support for streaming responses
- Add support for rate limiting and retries
- Add support for response caching
- Add support for model configuration validation
"""

from typing import Dict, List, Optional, Union
import openai

from shellsense.ai.prompts.instructions import system_prompt
from shellsense.config.settings import Config
from shellsense.ai.providers.base_provider import BaseProvider
from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)


class OpenAIProvider(BaseProvider):
    """
    Manages API interactions with OpenAI.
    Supports tool calling functionality.
    """

    @log_function_call
    def __init__(self):
        """Initialize OpenAIProvider with configuration."""
        try:
            Config.validate(provider="openai")
            self.api_key = Config.OPENAI_API_KEY
            openai.api_key = self.api_key
            logger.debug("OpenAIProvider initialized successfully")
        except ValueError as e:
            logger.error("Failed to initialize OpenAIProvider", extra={
                "error": str(e),
                "provider": "openai"
            })
            raise

    @log_function_call
    def supports_tool_calling(self) -> bool:
        """Check if provider supports tool calling."""
        return True

    @log_function_call
    def chat(self, messages: Union[str, List[Dict[str, str]]], model: Optional[str] = None) -> Union[str, Dict]:
        """
        Interacts with OpenAI's GPT models.

        Args:
            messages: Either a string prompt or a list of message dictionaries
            model: Optional model override for the API call

        Returns:
            Union[str, Dict]: The model's response

        Raises:
            ValueError: If OpenAI API key is not configured
            openai.error.OpenAIError: If the API request fails
        """
        try:
            if isinstance(messages, str):
                messages = [
                    {"role": "system", "content": system_prompt()},
                    {"role": "user", "content": messages},
                ]

            model = model or "gpt-3.5-turbo"
            logger.debug("Sending request to OpenAI API", extra={
                "model": model,
                "message_count": len(messages)
            })

            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )

            logger.debug("Received response from OpenAI API", extra={
                "model": model,
                "response_id": response.id,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            })

            return response.choices[0].message["content"]
        except openai.error.OpenAIError as e:
            logger.error("Failed to call OpenAI API", extra={
                "error": str(e),
                "model": model,
                "error_type": type(e).__name__
            })
            raise

    @log_function_call
    def get_tool_call_response(self, messages: List[Dict[str, str]], tools: List[Dict], model: Optional[str] = None) -> Dict:
        """
        Get response with tool calling support.

        Args:
            messages: List of message dictionaries
            tools: List of tool definitions
            model: Optional model override

        Returns:
            Dict: Response containing tool calls and/or content

        Raises:
            ValueError: If OpenAI API key is not configured
            openai.error.OpenAIError: If the API request fails
        """
        try:
            model = model or "gpt-3.5-turbo"
            logger.debug("Sending tool call request to OpenAI API", extra={
                "model": model,
                "message_count": len(messages),
                "tool_count": len(tools)
            })

            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            logger.debug("Received tool call response from OpenAI API", extra={
                "model": model,
                "response_id": response.id,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "has_tool_calls": bool(response.choices[0].message.get("tool_calls"))
            })

            return response
        except openai.error.OpenAIError as e:
            logger.error("Failed to call OpenAI API with tools", extra={
                "error": str(e),
                "model": model,
                "error_type": type(e).__name__,
                "tool_count": len(tools)
            })
            raise
