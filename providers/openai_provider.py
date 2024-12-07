import openai
from config.settings import Config


class OpenAIProvider:
    """
    Manages API interactions with OpenAI.
    """

    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        openai.api_key = self.api_key

    def chat(self, prompt: str) -> str:
        """
        Interacts with OpenAI's GPT models.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The model's response.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message["content"]
        except openai.error.OpenAIError as e:
            return f"Error: {e}"
