"""
Base class for AI providers.

This class defines the interface that all AI providers must implement.
It provides common functionality and enforces a consistent API across providers.

TODO:
- Add support for async operations
- Add support for streaming responses
- Add support for model configuration validation
- Add support for rate limiting and retries
- Add support for response caching
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)


class BaseProvider(ABC):
    """
    Abstract base class for AI providers.
    
    This class defines the interface that all AI providers must implement.
    It provides common functionality and enforces a consistent API across providers.
    """
    
    @abstractmethod
    def __init__(self):
        """Initialize the provider with configuration."""
        pass
    
    @abstractmethod
    @log_function_call
    def chat(self, messages: Union[str, List[Dict[str, str]]], model: Optional[str] = None) -> Union[str, Dict]:
        """
        Interact with the AI model.
        
        Args:
            messages: Either a string prompt or a list of message dictionaries
            model: Optional model override for the API call
            
        Returns:
            Union[str, Dict]: The model's response
            
        Raises:
            ValueError: If required configuration is missing
            Exception: If the API request fails
        """
        pass
    
    @abstractmethod
    @log_function_call
    def supports_tool_calling(self) -> bool:
        """
        Check if the provider supports tool calling.
        
        Returns:
            bool: True if tool calling is supported, False otherwise
        """
        pass

    @abstractmethod
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
            ValueError: If tool calling is not supported
            Exception: If the API request fails
        """
        pass
