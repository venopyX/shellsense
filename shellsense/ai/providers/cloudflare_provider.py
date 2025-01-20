"""
Manages API interactions with Cloudflare.
"""

import logging
from typing import Dict, List, Optional, Union

import requests
import json

from shellsense.config.settings import Config
from shellsense.ai.providers.base_provider import BaseProvider
from shellsense.ai.prompts.instructions import system_prompt, tool_caller_ai

logger = logging.getLogger(__name__)


class CloudflareProvider(BaseProvider):
    """
    Manages API interactions with Cloudflare.
    Supports tool calling functionality.
    """

    def __init__(self):
        """Initialize CloudflareProvider with configuration."""
        try:
            Config.validate(provider="cloudflare")
            self.api_token = Config.API_TOKEN
            self.api_url = Config.CLOUDFLARE_API_URL
            self.account_id = Config.ACCOUNT_ID
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise

    def supports_tool_calling(self) -> bool:
        """Check if provider supports tool calling."""
        return True

    def chat(self, messages: Union[str, List[Dict[str, str]]], model: Optional[str] = None) -> Union[str, Dict]:
        """
        Interacts with Cloudflare's AI models.

        Args:
            messages: Either a string prompt or a list of message dictionaries
            model: Optional model override for the API call

        Returns:
            Union[str, Dict]: The API's response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        if not model:
            model = Config.FUNCTION_CALL_MODEL

        api_url = (
            self.api_url
            if not model
            else f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{model}"
        )

        try:
            payload = {"messages": messages}
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }

            logger.debug(f"Sending request to Cloudflare API: {api_url}")
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Raw Cloudflare API response: {data}")
            
            # Extract response from Cloudflare format
            if "result" in data and "response" in data["result"]:
                return data["result"]["response"]
            elif "result" in data:
                return data["result"]
            else:
                logger.warning("Unexpected response format from Cloudflare")
                return data
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to call Cloudflare API: {str(e)}")
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
            requests.exceptions.RequestException: If the API request fails
        """
        if not model:
            model = Config.FUNCTION_CALL_MODEL

        api_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{model}"

        try:
            # Create tool names string for the prompt
            tool_names = [tool["name"] for tool in tools]
            tool_names_str = f"Available tools: {tool_names}"

            # Prepare messages with system instructions
            messages_with_tools = [
                {"role": "system", "content": f"This is system instruction for you to guide you: {system_prompt()}"},
                {"role": "system", "content": tool_caller_ai(tool_names_str)},
                *messages
            ]

            payload = {
                "messages": messages_with_tools,
                "tools": tools
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }

            logger.debug(f"Sending tool call request to Cloudflare API: {api_url}")
            logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Raw Cloudflare API tool call response: {data}")

            # Extract response and tool calls
            result = data.get("result", {})
            response_text = result.get("response", "")
            tool_calls = result.get("tool_calls", [])

            # Validate tool calls
            valid_tool_calls = []
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments", {})
                
                # Skip if tool doesn't exist
                if tool_name not in tool_names:
                    logger.warning(f"Tool '{tool_name}' not found in available tools")
                    continue

                # Find tool schema
                tool_schema = next((t for t in tools if t["name"] == tool_name), None)
                if not tool_schema:
                    logger.warning(f"Schema for tool '{tool_name}' not found")
                    continue

                # Validate required arguments
                required_args = tool_schema["parameters"].get("required", [])
                if not all(arg in arguments for arg in required_args):
                    logger.warning(f"Missing required arguments for tool '{tool_name}'")
                    continue

                valid_tool_calls.append({
                    "name": tool_name,
                    "arguments": arguments
                })

            # Return in standard format
            return {
                "result": {
                    "response": response_text if not valid_tool_calls else "",
                    "tool_calls": valid_tool_calls
                }
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to call Cloudflare API with tools: {str(e)}")
            raise
