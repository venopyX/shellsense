import requests
from config.settings import Config

class CloudflareProvider:
    """
    Manages API interactions with Cloudflare.
    """
    def __init__(self):
        self.account_id = Config.ACCOUNT_ID
        self.api_token = Config.API_TOKEN

    def chat(self, messages: list, model: str = None) -> dict:
        """
        Interacts with Cloudflare's AI function calling system.
        Args:
        messages (list): A list of message dictionaries for the API.
        model (str): The model to use for the API call.
        Returns:
        dict: The API's response.
        """
        if not model:
            model = Config.FUNCTION_CALL_MODEL
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{model}"
        payload = {"messages": messages}
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
