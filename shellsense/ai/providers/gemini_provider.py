"""
Manages API interactions with Google's Gemini API.

This module provides a GeminiProvider class that handles all interactions with
Google's Gemini API, including tool calling functionality.

TODO:
- Add support for streaming responses
- Add support for rate limiting and retries
- Add support for response caching
- Add support for model configuration validation
- Add support for better error handling
"""

from typing import Dict, List, Optional, Union

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration

from shellsense.ai.providers.base_provider import BaseProvider
from shellsense.config.settings import Config
from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)


class GeminiProvider(BaseProvider):
    """
    Manages API interactions with Google's Gemini API.
    Supports tool calling functionality.
    """

    @log_function_call
    def __init__(self):
        """Initialize GeminiProvider with configuration."""
        try:
            Config.validate(provider="gemini")
            self.api_key = Config.GEMINI_API_KEY
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.debug("GeminiProvider initialized successfully", extra={
                "model": "gemini-pro"
            })
        except ValueError as e:
            logger.error("Failed to initialize GeminiProvider", extra={
                "error": str(e),
                "provider": "gemini"
            })
            raise

    @log_function_call
    def supports_tool_calling(self) -> bool:
        """Check if provider supports tool calling."""
        return True

    @log_function_call
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

        logger.debug("Converted schema to Gemini format", extra={
            "original_keys": list(schema.keys()),
            "cleaned_keys": list(cleaned_schema.keys())
        })

        return cleaned_schema

    @log_function_call
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

            logger.debug("Sending request to Gemini API", extra={
                "content_length": len(content),
                "message_type": "string" if isinstance(messages, str) else "list"
            })

            response = self.model.generate_content(content)

            logger.debug("Received response from Gemini API", extra={
                "response_length": len(response.text) if hasattr(response, 'text') else 0,
                "has_candidates": bool(response.candidates) if hasattr(response, 'candidates') else False
            })

            return response.text
        except Exception as e:
            logger.error("Failed to call Gemini API", extra={
                "error": str(e),
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
                        logger.warning("Invalid tool schema", extra={
                            "tool": str(tool)
                        })
                        continue
                        
                    parameters_schema = self._convert_schema_to_gemini(tool["parameters"])
                    function_declarations.append({
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": parameters_schema
                    })
                except Exception as e:
                    logger.warning("Failed to convert tool schema", extra={
                        "tool_name": tool.get('name', 'unknown'),
                        "error": str(e),
                        "error_type": type(e).__name__
                    })
                    continue

            logger.debug("Prepared function declarations", extra={
                "total_tools": len(tools),
                "valid_declarations": len(function_declarations)
            })

            # Convert messages to Gemini format with explicit tool usage instruction
            content = "You are a helpful AI assistant with access to various tools. When a user asks for information that requires using tools, ALWAYS use the appropriate tool instead of saying you can't help.\n\n"
            content += "Available tools and their purposes:\n"
            for tool in tools:
                content += f"- {tool['name']}: {tool.get('description', '').split('.')[0]}.\n"
            content += "\nUser request:\n"
            content += "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)

            logger.debug("Sending tool call request to Gemini API", extra={
                "content_length": len(content),
                "message_count": len(messages),
                "tool_count": len(function_declarations)
            })

            # Create request with tools
            response = self.model.generate_content(
                content,
                tools=[{"function_declarations": function_declarations}],
                tool_config={"function_calling_config": {"mode": "AUTO"}}
            )

            logger.debug("Received tool call response from Gemini API", extra={
                "has_candidates": bool(response.candidates) if hasattr(response, 'candidates') else False
            })

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
                                            logger.warning("Failed to convert function args to dict", extra={
                                                "error": str(e),
                                                "args_type": type(function_call.args).__name__
                                            })
                                
                                result["result"]["tool_calls"].append({
                                    "name": str(function_call.name),
                                    "arguments": args
                                })

                # Clean up response text
                result["result"]["response"] = result["result"]["response"].strip()

                logger.info("Successfully processed Gemini response", extra={
                    "response_length": len(result["result"]["response"]),
                    "tool_call_count": len(result["result"]["tool_calls"])
                })

            except Exception as e:
                logger.warning("Error extracting response content", extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                })
                # Use string representation as fallback
                result["result"]["response"] = str(response)

            return result
        except Exception as e:
            logger.error("Failed to call Gemini API with tools", extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "tool_count": len(tools)
            })
            raise
