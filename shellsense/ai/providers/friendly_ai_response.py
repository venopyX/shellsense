import logging
from shellsense.config.settings import Config
from shellsense.ai.prompts.instructions import friendly_ai, system_prompt
from shellsense.ai.providers.cloudflare_provider import CloudflareProvider

logger = logging.getLogger(__name__)

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
        try:
            logger.info("Generating friendly response for user query")
            messages = [
                {"role": "system", "content": system_prompt()},
                {"role": "system", "content": friendly_ai()},
                {"role": "user", "content": f"User Query: {user_query}"},
                {"role": "assistant", "content": f"Tool Responses: {tool_output}"},
            ]
            response = self.cloudflare_provider.chat(messages, model=self.friendly_response_model)
            logger.debug("Successfully generated friendly response")
            return response.get("result", {}).get("response", "No response generated.")
        except Exception as e:
            logger.error(f"Failed to generate friendly response: {str(e)}")
            return f"Error generating response: {str(e)}"
