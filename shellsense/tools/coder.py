import logging
from shellsense.tools.base import BaseTool
from shellsense.ai.providers.cloudflare_provider import CloudflareProvider
from shellsense.ai.prompts.instructions import coder_ai

logger = logging.getLogger(__name__)

class CoderTool(BaseTool):
    """
    Generates concise, well-structured code snippets based on user input.
    """

    def __init__(self):
        self.cloudflare_provider = CloudflareProvider()

    def invoke(self, input: dict) -> dict:
        """
        Generates code based on the provided language and description.

        Args:
            input (dict): Contains 'language' and 'description' for code generation.

        Returns:
            dict: Generated code snippet or error message.

        Raises:
            KeyError: If required parameters are missing.
        """
        try:
            language = input.get("language")
            description = input.get("description")

            if not language or not description:
                logger.error("Missing required parameters")
                return {"error": "Parameters 'language' and 'description' are required."}

            logger.info(f"Generating {language} code snippet")
            prompt = f"Generate a {language} code snippet for: {description}"
            messages = [
                {"role": "system", "content": coder_ai()},
                {"role": "user", "content": prompt},
            ]

            response = self.cloudflare_provider.chat(messages)
            if response.get("error"):
                logger.error(f"Failed to generate code: {response['error']}")
                return {"error": response["error"]}

            code_snippet = response.get("result", {}).get("response", "No code generated.")
            logger.debug("Successfully generated code snippet")
            print(f"CODE: {code_snippet}")
            return {"code_snippet": code_snippet}

        except Exception as e:
            logger.error(f"Unexpected error in code generation: {str(e)}")
            return {"error": f"Failed to generate code: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the CoderTool's input parameters.

        Returns:
            dict: JSON schema for validation and documentation.
        """
        return {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "description": "Programming language for code generation"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the code to generate"
                }
            },
            "required": ["language", "description"]
        }
