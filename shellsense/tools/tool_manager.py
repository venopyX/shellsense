"""
Tool manager for handling tool initialization, schema preparation, and execution.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from shellsense.ai.prompts import system_prompt, tool_caller_ai
from shellsense.ai.providers.base_provider import BaseProvider
from shellsense.ai.providers.cloudflare_provider import CloudflareProvider
from shellsense.ai.providers.openai_provider import OpenAIProvider
from shellsense.ai.providers.gemini_provider import GeminiProvider
from shellsense.ai.providers.friendly_ai_response import FriendlyAiResponse
from shellsense.config.settings import Config
from shellsense.tools import (CoderTool,  # WikipediaSearchTool,
                              CommandExecutionTool, CrawlerTool, GitHubTool,
                              ProductHuntTool, ScreenshotTool, StockTool,
                              TranslatorTool, WebSearchTool)
from shellsense.utils.futuristic_loading import FuturisticLoading

logger = logging.getLogger(__name__)
loader = FuturisticLoading()


class ToolManager:
    """
    Manages tool initialization, schema preparation, and execution.

    This class is responsible for loading tools, preparing their schemas,
    and processing user queries by coordinating between tools and AI providers.
    """

    def __init__(self, provider: str = "cloudflare"):
        """
        Initialize ToolManager with configuration and tools.
        
        Args:
            provider: AI provider to use (cloudflare, openai, or gemini)
        """
        try:
            # Load and validate config for the selected provider
            config = Config()
            config.update_from_dict(os.environ)
            config.validate(provider=provider)

            self.provider = self._initialize_provider(provider)
            logger.info("Initializing ToolManager")
            self.tool_mapping = self.load_tools()
            self.friendly_ai_response = FriendlyAiResponse()
            logger.debug(f"Initialized {len(self.tool_mapping)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize ToolManager: {e}")
            raise

    def _initialize_provider(self, provider: str) -> BaseProvider:
        """Initialize the selected AI provider."""
        providers = {
            "cloudflare": CloudflareProvider,
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
        }
        
        if provider not in providers:
            raise ValueError(f"Invalid provider: {provider}. Available providers: {list(providers.keys())}")
            
        return providers[provider]()

    def load_tools(self) -> Dict[str, Any]:
        """
        Load all available tools into the tool mapping.

        Returns:
            Dict[str, Any]: Mapping of tool names to tool instances
        """
        logger.debug("Loading tools")
        tools = {
            "executeShellCommands": CommandExecutionTool(),
            "getGithubUserInfo": GitHubTool(),
            "getCurrentStockPrice": StockTool(),
            "performWebSearch": WebSearchTool(),
            "scrapeVisibleText": CrawlerTool(),
            "getProductHuntTrending": ProductHuntTool(),
            "takeScreenshotOfWebPage": ScreenshotTool(),
            "translateText": TranslatorTool(),
            # "wikipediaSearch": WikipediaSearchTool(),
            "generateCode": CoderTool(),
        }
        logger.debug(f"Loaded tools: {list(tools.keys())}")
        return tools

    def prepare_tools_schema(self) -> List[Dict[str, Any]]:
        """
        Prepare the tools schema for AI providers.

        Returns:
            List[Dict[str, Any]]: List of tool schemas
        """
        logger.debug("Preparing tool schemas")
        tools_schema = []
        for tool_name, tool_instance in self.tool_mapping.items():
            schema = {
                "name": tool_name,
                "description": tool_instance.__doc__,
                "parameters": tool_instance.get_schema(),
            }
            tools_schema.append(schema)
            logger.debug(f"Prepared schema for tool '{tool_name}'")

        logger.debug(f"Tool schemas: {json.dumps(tools_schema, indent=2)}")
        return tools_schema

    def process_query(self, query: str) -> str:
        """
        Process a user query using the configured AI provider.

        Args:
            query: The user's query

        Returns:
            str: The response from the AI provider

        Raises:
            Exception: If there is an error processing the query
        """
        try:
            logger.info(f"Processing user query: {query}")
            logger.debug(f"Available tools: {list(self.tool_mapping.keys())}")

            # Prepare tool schemas
            tool_schemas = self.prepare_tools_schema()
            logger.debug(f"Tool schemas: {json.dumps(tool_schemas, indent=2)}")

            # Add system instructions to messages
            messages = [
                {"role": "user", "content": query}
            ]

            # Get response from provider
            logger.info(f"Sending request to {self.provider.__class__.__name__}")
            response = self.provider.get_tool_call_response(
                messages=messages,
                tools=tool_schemas,
            )

            # Log response safely
            try:
                logger.debug(f"Provider response: {json.dumps(response, indent=2)}")
            except TypeError:
                logger.debug(f"Provider response (non-JSON): {str(response)}")

            # Process tool calls
            tool_calls = response.get("result", {}).get("tool_calls", [])
            if tool_calls:
                logger.info(f"Processing {len(tool_calls)} tool calls")
                loading_text = "Using tools..."
                logger.debug(f"Updating loading text to: {loading_text}")
                loader.text(loading_text)

                # Execute each tool call and collect outputs
                tool_outputs = []
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    arguments = tool_call.get("arguments")

                    if not tool_name:
                        logger.debug("Skipping empty tool call")
                        continue

                    logger.debug(f"Executing tool '{tool_name}' with arguments: {arguments}")
                    raw_output = self.call_tool(tool_name, arguments)
                    
                    # Sanitize and format the output
                    if isinstance(raw_output, (dict, list)):
                        try:
                            output = json.dumps(raw_output, ensure_ascii=False)
                        except Exception as e:
                            logger.warning(f"Failed to JSON encode output: {e}")
                            output = str(raw_output)
                    else:
                        output = str(raw_output)

                    tool_outputs.append(f"Tool {tool_name} output:\n{output}")

                # Combine tool outputs with simple newlines
                combined_output = "\n\n".join(tool_outputs)

                # Get friendly response
                friendly_response = self.friendly_ai_response.get_friendly_response(
                    user_query=query,
                    tool_output=combined_output
                )

                return friendly_response

            # If no tool calls, just return the response text
            return response.get("result", {}).get("response", "")

        except Exception as e:
            logger.error(f"Failed to process query: {str(e)}")
            raise

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the corresponding tool function based on the tool name.

        Args:
            tool_name (str): Name of the tool to call
            arguments (dict): Arguments to pass to the tool

        Returns:
            dict: Result from the tool function

        Raises:
            KeyError: If the tool is not found
            Exception: If the tool execution fails
        """
        try:
            tool_instance = self.tool_mapping.get(tool_name)
            if not tool_instance:
                logger.error(f"Tool '{tool_name}' not found in tool mapping")
                return {"error": f"Tool '{tool_name}' not found"}

            # Get tool schema
            schema = {
                "name": tool_name,
                "description": tool_instance.__doc__,
                "parameters": tool_instance.get_schema()
            }

            # Validate required arguments
            required_args = schema["parameters"].get("required", [])
            if not all(arg in arguments for arg in required_args):
                missing_args = [arg for arg in required_args if arg not in arguments]
                logger.error(f"Missing required arguments for tool '{tool_name}': {missing_args}")
                return {"error": f"Missing required arguments: {missing_args}"}

            logger.debug(f"Invoking tool '{tool_name}' with arguments: {arguments}")
            result = tool_instance.invoke(arguments)
            logger.debug(f"Tool '{tool_name}' result: {result}")
            return result

        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return {"error": f"Failed to execute tool '{tool_name}': {str(e)}"}
