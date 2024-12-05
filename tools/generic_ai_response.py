# tools/generic_ai_response.py

from tools.base_tool import BaseTool
from utils.friendly_ai import FriendlyAiResponse

class GenericAiResponseTool(BaseTool):
    """
    Sends a user's query directly to the AI API for a natural, human-like response.
    """

    def invoke(self, input: dict) -> dict:
        user_query = input.get("query")

        if not user_query:
            return {"error": "Query parameter is required."}

        try:
            # Use FriendlyAiResponse to get a direct AI response for the user's query
            ai_response = FriendlyAiResponse.get_friendly_response(user_query, tool_output="")
            return {"response": ai_response}

        except Exception as e:
            return {"error": f"Failed to get AI response: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the generic AI response tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The normal user query for which a response is needed."
                }
            },
            "required": ["query"]
        }
