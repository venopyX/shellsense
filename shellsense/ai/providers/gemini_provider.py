"""
Manages API interactions with Google's Gemini API.
"""

import logging
from typing import Dict, List, Optional, Union

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration

from shellsense.ai.providers.base_provider import BaseProvider
from shellsense.config.settings import Config

logger = logging.getLogger(__name__)


class GeminiProvider(BaseProvider):
    """
    Manages API interactions with Google's Gemini API.
    Supports tool calling functionality.
    """

    def __init__(self):
        """Initialize GeminiProvider with configuration."""
        try:
            Config.validate(provider="gemini")
            self.api_key = Config.GEMINI_API_KEY
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise

    def supports_tool_calling(self) -> bool:
        """Check if provider supports tool calling."""
        return True

    def _convert_schema_to_gemini(self, schema: Dict) -> Dict:
        """
        Convert JSON Schema to Gemini Schema format.
        
        Args:
            schema: JSON Schema dictionary
            
        Returns:
            Dict: Cleaned schema dictionary for Gemini
        """
        # Remove unsupported fields
        cleaned_schema = {}
        
        # Handle type
        if "type" in schema:
            cleaned_schema["type"] = schema["type"].upper()  # Gemini expects uppercase types

        # Handle properties
        if "properties" in schema:
            properties = {}
            for prop_name, prop_schema in schema["properties"].items():
                prop_cleaned = self._convert_schema_to_gemini(prop_schema)
                properties[prop_name] = prop_cleaned
            cleaned_schema["properties"] = properties

        # Handle required fields
        if "required" in schema:
            cleaned_schema["required"] = schema["required"]

        # Handle array items
        if "items" in schema and schema.get("type") == "array":
            cleaned_schema["items"] = self._convert_schema_to_gemini(schema["items"])

        # Handle description
        if "description" in schema:
            cleaned_schema["description"] = schema["description"]

        # Handle enum
        if "enum" in schema:
            cleaned_schema["enum"] = schema["enum"]

        return cleaned_schema

    def chat(self, messages: Union[str, List[Dict[str, str]]], model: Optional[str] = None) -> Union[str, Dict]:
        """
        Interacts with Gemini's models.

        Args:
            messages: Either a string prompt or a list of message dictionaries
            model: Optional model override (not used for Gemini)

        Returns:
            Union[str, Dict]: The model's response

        Raises:
            ValueError: If Gemini API key is not configured
            Exception: If the API request fails
        """
        try:
            # Convert messages to Gemini format
            if isinstance(messages, str):
                content = messages
            else:
                # Combine messages into a single string, maintaining context
                content = "\n".join(
                    f"{msg['role']}: {msg['content']}" for msg in messages
                )

            response = self.model.generate_content(content)
            return response.text
        except Exception as e:
            logger.error(f"Failed to call Gemini API: {e}")
            raise

    def get_tool_call_response(self, messages: List[Dict[str, str]], tools: List[Dict], model: Optional[str] = None) -> Dict:
        """
        Get response with tool calling support.

        Args:
            messages: List of message dictionaries
            tools: List of tool definitions
            model: Optional model override (not used for Gemini)

        Returns:
            Dict: Response containing tool calls and/or content

        Raises:
            ValueError: If Gemini API key is not configured
            Exception: If the API request fails
        """
        try:
            # Convert tools to Gemini function declarations
            function_declarations = []
            for tool in tools:
                try:
                    if not isinstance(tool, dict) or 'name' not in tool or 'parameters' not in tool:
                        logger.warning(f"Invalid tool schema: {tool}")
                        continue
                        
                    parameters_schema = self._convert_schema_to_gemini(tool["parameters"])
                    function_declarations.append({
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": parameters_schema
                    })
                except Exception as e:
                    logger.warning(f"Failed to convert tool {tool.get('name', 'unknown')}: {e}")
                    continue

            # Convert messages to Gemini format with explicit tool usage instruction
            content = "You are a helpful AI assistant with access to various tools. When a user asks for information that requires using tools, ALWAYS use the appropriate tool instead of saying you can't help.\n\n"
            content += "Available tools and their purposes:\n"
            for tool in tools:
                content += f"- {tool['name']}: {tool.get('description', '').split('.')[0]}.\n"
            content += "\nUser request:\n"
            content += "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)

            # Create request with tools
            response = self.model.generate_content(
                content,
                tools=[{"function_declarations": function_declarations}],
                tool_config={"function_calling_config": {"mode": "AUTO"}}
            )

            # Convert Gemini response to standard format
            result = {
                "result": {
                    "response": "",
                    "tool_calls": []
                }
            }

            # Extract text and function calls from response
            try:
                if response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content:
                        # Process each part of the response
                        for part in candidate.content.parts:
                            # Extract text
                            if hasattr(part, 'text') and part.text:
                                result["result"]["response"] += part.text + " "
                            
                            # Extract function calls
                            if hasattr(part, 'function_call') and part.function_call:
                                # Convert function call to dict for JSON serialization
                                function_call = part.function_call
                                args = {}
                                if hasattr(function_call, 'args') and function_call.args:
                                    if isinstance(function_call.args, dict):
                                        args = function_call.args
                                    else:
                                        # Try to convert args to dict if it's not already
                                        try:
                                            args = dict(function_call.args)
                                        except Exception as e:
                                            logger.warning(f"Failed to convert function args to dict: {e}")
                                
                                result["result"]["tool_calls"].append({
                                    "name": str(function_call.name),
                                    "arguments": args
                                })

                # Clean up response text
                result["result"]["response"] = result["result"]["response"].strip()

            except Exception as e:
                logger.warning(f"Error extracting response content: {e}")
                # Use string representation as fallback
                result["result"]["response"] = str(response)

            return result
        except Exception as e:
            logger.error(f"Failed to call Gemini API with tools: {e}")
            raise
