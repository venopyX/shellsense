import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """
    Abstract Base Class for all tools.
    Each tool must implement the `invoke` method and provide a schema.
    """

    @abstractmethod
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the tool with the given input.

        Args:
            input_data (Dict[str, Any]): Input parameters for the tool.

        Returns:
            Dict[str, Any]: The result of the tool's execution.

        Raises:
            NotImplementedError: If the child class doesn't implement this method.
            ValueError: If input parameters are invalid.
        """
        raise NotImplementedError("Tool must implement invoke method")

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the tool's input parameters.
        Override this method to provide a specific schema for your tool.

        Returns:
            Dict[str, Any]: JSON schema definition with properties and requirements.

        Example schema:
            {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Description of param1"
                    }
                },
                "required": ["param1"]
            }
        """
        logger.warning("Using default schema. Tool should override get_schema method.")
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate input data against the tool's schema.
        Override this method to add custom validation logic.

        Args:
            input_data (Dict[str, Any]): Input data to validate.

        Raises:
            ValueError: If input data is invalid.
        """
        schema = self.get_schema()
        required = schema.get("required", [])
        
        # Check required fields
        for field in required:
            if field not in input_data:
                logger.error(f"Missing required field: {field}")
                raise ValueError(f"Missing required field: {field}")

        # Check field types if specified
        properties = schema.get("properties", {})
        for field, value in input_data.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type == "string" and not isinstance(value, str):
                    logger.error(f"Field {field} must be a string")
                    raise ValueError(f"Field {field} must be a string")
                elif expected_type == "number" and not isinstance(value, (int, float)):
                    logger.error(f"Field {field} must be a number")
                    raise ValueError(f"Field {field} must be a number")
                elif expected_type == "boolean" and not isinstance(value, bool):
                    logger.error(f"Field {field} must be a boolean")
                    raise ValueError(f"Field {field} must be a boolean")
                elif expected_type == "array" and not isinstance(value, list):
                    logger.error(f"Field {field} must be an array")
                    raise ValueError(f"Field {field} must be an array")
