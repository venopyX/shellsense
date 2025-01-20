from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Abstract Base Class for all tools.
    Each tool must implement the `invoke` method.
    """

    @abstractmethod
    def invoke(self, input: dict) -> dict:
        """
        Invoke the tool with the given input.

        Args:
            input (dict): Input parameters for the tool.

        Returns:
            dict: The result of the tool's execution.
        """
        pass

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the tool's input parameters.

        Returns:
            dict: JSON schema definition following Cloudflare API requirements.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {},
            "required": [],
        }
