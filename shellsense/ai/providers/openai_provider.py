import logging
import openai
from shellsense.config.settings import Config
from shellsense.ai.prompts.instructions import system_prompt

logger = logging.getLogger(__name__)

class OpenAIProvider:
    """
    Manages API interactions with OpenAI.
    """

    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        openai.api_key = self.api_key

    def chat(self, prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
        """
        Interacts with OpenAI's GPT models.

        Args:
            prompt (str): The input prompt for the model.
            model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
            temperature (float, optional): Controls randomness in the response. Defaults to 0.7.

        Returns:
            str: The model's response.

        Raises:
            openai.error.OpenAIError: If the API request fails.
        """
        try:
            logger.info(f"Making request to OpenAI API with model: {model}")
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )
            logger.debug("Successfully received response from OpenAI API")
            return response.choices[0].message["content"]
        except openai.error.OpenAIError as e:
            logger.error(f"Failed to make request to OpenAI API: {str(e)}")
            return f"Error: {e}"
