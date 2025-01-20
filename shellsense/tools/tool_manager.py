"""
Tool manager for handling tool initialization, schema preparation, and execution.
"""

import json
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
from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)
loader = FuturisticLoading()


class ToolManager:
    """
    Manages tool initialization, schema preparation, and execution.

    This class is responsible for loading tools, preparing their schemas,
    and processing user queries by coordinating between tools and AI providers.
    """

    @log_function_call
    def __init__(self, provider: str = "cloudflare"):
        """
        Initialize ToolManager with configuration and tools.
        
        Args:
            provider: AI provider to use (cloudflare, openai, or gemini)
        """
        try:
            logger.info("Initializing ToolManager", extra={"provider": provider})
            
            # Load and validate config for the selected provider
            config = Config()
            config.update_from_dict(os.environ)
            config.validate(provider=provider)
            logger.debug("Configuration loaded and validated successfully")

            self.provider = self._initialize_provider(provider)
            self.tool_mapping = self.load_tools()
            self.friendly_ai_response = FriendlyAiResponse()
            
            logger.info("ToolManager initialized successfully", 
                       extra={"tool_count": len(self.tool_mapping)})
        except Exception as e:
            logger.error("Failed to initialize ToolManager", 
                        extra={"error": str(e), "provider": provider}, 
                        exc_info=True)
            raise

    @log_function_call
    def _initialize_provider(self, provider: str) -> BaseProvider:
        """Initialize the selected AI provider."""
        providers = {
            "cloudflare": CloudflareProvider,
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
        }
        
        if provider not in providers:
            logger.error("Invalid provider specified", 
                        extra={"provider": provider, 
                              "available_providers": list(providers.keys())})
            raise ValueError(f"Invalid provider: {provider}. Available providers: {list(providers.keys())}")
        
        logger.info(f"Initializing AI provider", extra={"provider": provider})    
        return providers[provider]()

    @log_function_call
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
        logger.info("Tools loaded successfully", extra={"tools": list(tools.keys())})
        return tools

    @log_function_call
    def prepare_tools_schema(self) -> List[Dict[str, Any]]:
        """
        Prepare the tools schema for AI providers.

        Returns:
            List[Dict[str, Any]]: List of tool schemas
        """
        logger.debug("Preparing tool schemas")
        tools_schema = []
        
        for tool_name, tool_instance in self.tool_mapping.items():
            try:
                schema = {
                    "name": tool_name,
                    "description": tool_instance.__doc__,
                    "parameters": tool_instance.get_schema(),
                }
                tools_schema.append(schema)
                logger.debug(f"Schema prepared successfully", 
                           extra={"tool": tool_name})
            except Exception as e:
                logger.error(f"Failed to prepare schema", 
                           extra={"tool": tool_name, "error": str(e)},
                           exc_info=True)

        logger.info("Tool schemas prepared successfully", 
                   extra={"schema_count": len(tools_schema)})
        return tools_schema

    @log_function_call
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
            logger.info("Processing user query", extra={"query": query})

            # Prepare tool schemas
            tool_schemas = self.prepare_tools_schema()

            # Add system instructions to messages
            messages = [
                {"role": "user", "content": query}
            ]

            # Get response from provider
            logger.info("Sending request to AI provider", 
                       extra={"provider": self.provider.__class__.__name__})
            response = self.provider.get_tool_call_response(
                messages=messages,
                tools=tool_schemas,
            )

            # Process tool calls
            tool_calls = response.get("result", {}).get("tool_calls", [])
            if tool_calls:
                logger.info("Processing tool calls", 
                           extra={"tool_call_count": len(tool_calls)})
                loading_text = "Using tools..."
                loader.text(loading_text)

                # Execute each tool call and collect outputs
                tool_outputs = []
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    arguments = tool_call.get("arguments")

                    if not tool_name:
                        logger.warning("Empty tool call received, skipping")
                        continue

                    logger.debug("Executing tool", 
                               extra={"tool": tool_name, "arguments": arguments})
                    raw_output = self.call_tool(tool_name, arguments)
                    
                    # Sanitize and format the output
                    if isinstance(raw_output, (dict, list)):
                        try:
                            output = json.dumps(raw_output, ensure_ascii=False)
                        except Exception as e:
                            logger.warning("Failed to JSON encode output", 
                                         extra={"error": str(e)},
                                         exc_info=True)
                            output = str(raw_output)
                    else:
                        output = str(raw_output)

                    tool_outputs.append(f"Tool {tool_name} output:\n{output}")

                # Combine tool outputs
                combined_output = "\n\n".join(tool_outputs)

                # Get friendly response
                logger.debug("Getting friendly response")
                friendly_response = self.friendly_ai_response.get_friendly_response(
                    user_query=query,
                    tool_output=combined_output
                )
                logger.info("Query processed successfully")
                return friendly_response

            # If no tool calls, just return the response text
            logger.info("No tool calls required, returning direct response")
            return response.get("result", {}).get("response", "")

        except Exception as e:
            logger.error("Failed to process query", 
                        extra={"error": str(e), "query": query},
                        exc_info=True)
            raise

    @log_function_call
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
                logger.error("Tool not found", extra={"tool": tool_name})
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
                logger.error("Missing required arguments", 
                           extra={"tool": tool_name, "missing_args": missing_args})
                return {"error": f"Missing required arguments: {missing_args}"}

            logger.debug("Invoking tool", 
                        extra={"tool": tool_name, "arguments": arguments})
            result = tool_instance.invoke(arguments)
            logger.debug("Tool execution completed", 
                        extra={"tool": tool_name, "result": result})
            return result

        except Exception as e:
            logger.error("Tool execution failed", 
                        extra={"tool": tool_name, "error": str(e)},
                        exc_info=True)
            return {"error": f"Failed to execute tool '{tool_name}': {str(e)}"}
