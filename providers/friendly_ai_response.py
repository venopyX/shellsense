from config.settings import Config
from prompts import friendly_ai
from providers.cloudflare_provider import CloudflareProvider

class FriendlyAiResponse:
    """
    Generates user-friendly responses using Cloudflare's AI API.
    """
    def __init__(self):
        self.api_token = Config.API_TOKEN
        self.friendly_response_model = Config.FRIENDLY_RESPONSE_MODEL
        self.cloudflare_provider = CloudflareProvider()

    def get_friendly_response(self, user_query: str, tool_output: str) -> str:
        """
        Refines raw tool output into a user-friendly response.
        Args:
        user_query (str): The user's original query.
        tool_output (str): Raw output from tools.
        Returns:
        str: A refined, user-friendly response.
        """
        messages = [
            {"role": "system", "content": friendly_ai()},
            {"role": "user", "content": f"User Query: {user_query}"},
            {"role": "assistant", "content": f"Tool Responses: {tool_output}"},
        ]
        response = self.cloudflare_provider.chat(messages, model=self.friendly_response_model)
        return response.get("result", {}).get("response", "No response generated.")
