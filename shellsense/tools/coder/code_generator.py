from shellsense.ai.prompts import coder_ai_prompt
from shellsense.ai.providers.cloudflare_provider import CloudflareProvider
from shellsense.tools.base_tool import BaseTool


class CoderTool(BaseTool):
    """
    Generates code snippets based on language and description inputs.

    Args:
    input (dict): Dictionary containing:
        - 'language' (str): Programming language for the code snippet (e.g., Python).
        - 'description' (str): Detailed description of the desired functionality.
    """

    def __init__(self):
        self.cloudflare_provider = CloudflareProvider()

    def invoke(self, input: dict) -> dict:
        """
        Generates a code snippet based on the specified language and description.

        Args:
            input (dict): Dictionary containing:
                - 'language' (str): Programming language for the code snippet (e.g., Python).
                - 'description' (str): Detailed description of the desired functionality.

        Returns:
            dict: Generated code snippet or an error message if inputs are missing.
        """
        language = input.get("language")
        description = input.get("description")

        if not language or not description:
            return {"error": "Both 'language' and 'description' are required."}

        prompt = f"Generate a {language} code snippet for: {description}"
        messages = [
            {"role": "system", "content": coder_ai_prompt()},
            {"role": "user", "content": prompt},
        ]

        response = self.cloudflare_provider.chat(messages)
        if response.get("error"):
            return {"error": response["error"]}

        code_snippet = response.get("result", {}).get("response", "No code generated.")
        print(f"CODE: {code_snippet}")
        return {"code_snippet": code_snippet}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the CoderTool's input parameters.

        Returns:
            dict: JSON schema for validating input parameters.
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
                    "description": "Description of the functionality for the code.",
                },
            },
            "required": ["language", "description"],
        }
