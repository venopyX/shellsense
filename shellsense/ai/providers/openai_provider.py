"""
Manages API interactions with OpenAI.
"""

import logging
from typing import Dict, List, Optional, Union

import openai

from shellsense.ai.prompts.instructions import system_prompt
from shellsense.config.settings import Config
from shellsense.ai.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseProvider):
    """
    Manages API interactions with OpenAI.
    Supports tool calling functionality.
    """

    def __init__(self):
        """Initialize OpenAIProvider with configuration."""
        try:
            Config.validate(provider="openai")
            self.api_key = Config.OPENAI_API_KEY
            openai.api_key = self.api_key
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise

    def supports_tool_calling(self) -> bool:
        """Check if provider supports tool calling."""
        return True

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
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message["content"]
        except openai.error.OpenAIError as e:
            logger.error(f"Failed to call OpenAI API: {e}")
            raise

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
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            return response
        except openai.error.OpenAIError as e:
            logger.error(f"Failed to call OpenAI API with tools: {e}")
            raise
