from tools.base_tool import BaseTool
from providers.cloudflare_provider import CloudflareProvider
from prompts import coder_ai


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
            dict: Generated code snippet or error.
        """
        language = input.get("language")
        description = input.get("description")

        if not language or not description:
            return {"error": "Parameters 'language' and 'description' are required."}

        prompt = f"Generate a {language} code snippet for: {description}"
        messages = [
            {"role": "system", "content": coder_ai()},
            {"role": "user", "content": prompt},
        ]

        response = self.cloudflare_provider.chat(messages)
        if response.get("error"):
            return {"error": response["error"]}
        print(f"CODE: {response.get("result", {}).get("response", "No code generated.")}")
        return {"code_snippet": response.get("result", {}).get("response", "No code generated.")}

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
                    "description": "Programming language for the code snippet (e.g., Python, JavaScript).",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the desired functionality for the code.",
                },
            },
            "required": ["language", "description"],
        }
