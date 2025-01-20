"""
Base class for AI providers.
"""

from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

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
    def supports_tool_calling(self) -> bool:
        """
        Check if the provider supports tool calling.
        
        Returns:
            bool: True if tool calling is supported, False otherwise
        """
        pass

    @abstractmethod
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
