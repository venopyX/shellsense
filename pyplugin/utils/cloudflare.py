# utils/cloudflare.py

import requests
from config.settings import Config

class CloudflareAPI:
    """
    Manages API interactions with Cloudflare Function Calling.
    """

    @staticmethod
    def call_api(messages: list, tools: list):
        """
        Calls the Cloudflare Function API with user messages and tool schemas.

        Args:
            messages (list): List of message dictionaries containing user queries.
            tools (list): List of tool schema dictionaries.

        Returns:
            dict: The response from Cloudflare's API.
        """
        payload = {
            "messages": messages,
            "tools": tools,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.API_TOKEN}",
        }

        try:
            response = requests.post(Config.CLOUDFLARE_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except Exception as err:
            print(f"Other error occurred: {err}")
            return {"error": str(err)}
