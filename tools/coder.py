# tools/coder.py

import requests
from config.settings import Config
from tools.base_tool import BaseTool

class CoderTool(BaseTool):
    """
    Generates code snippets using the specified programming language and description.
    """

    def invoke(self, input: dict) -> dict:
        language = input.get("language")
        description = input.get("description")

        if not language or not description:
            return {"error": "Parameters 'language' and 'description' are required."}

        try:
            headers = {"Authorization": f"Bearer {Config.API_TOKEN}"}
            prompt = f"Generate a concise and well-structured {language} code snippet for the following \
            description: {description}."

            response = requests.post(
                f"{Config.API_BASE_URL}@hf/mistral/mistral-7b-instruct-v0.2",
                headers=headers,
                json={
                    "max_tokens": 2048,
                    "messages": [
                        {"role": "system", "content": "You are code-generating assistant.\
                        Use best algorithm, and make it clean code, use short and brief docstrings.\
                        Do not include comments in the code.\
                        Output only desired code generated(use code-block always)\
                        Nothing outside the code-block."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            result = response.json()
            code_snippet = result.get("result", {}).get("response", "Failed to generate code.")

            # print("code_snippet"+ code_snippet)
            return {"code_snippet": code_snippet}

        except Exception as e:
            return {"error": f"Code generation failed: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the coder tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "description": "The programming language to generate the code snippet in."
                },
                "description": {
                    "type": "string",
                    "description": "The description of the code snippet to generate, Never suggest to add anything except the desired code."
                }
            },
            "required": ["language", "description"]
        }
