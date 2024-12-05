import os
import requests
import openai
from config.config_loader import load_env
from pyplugin.utils.instruction import Instruction

class OpenAIProvider:
    def __init__(self):
        env = load_env()
        self.api_key = env["OPENAI_API_KEY"]
        openai.api_key = self.api_key

    def chat(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": Instruction.shellsense_ai()},
                {"role": "user", "content": prompt}
                ],
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"

class CloudflareProvider:
    def __init__(self):
        env = load_env()
        self.account_id = env.get("CLOUDFLARE_ACCOUNT_ID")
        self.auth_token = env.get("CLOUDFLARE_AUTH_TOKEN")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@hf/thebloke/llama-2-13b-chat-awq"

    def chat(self, prompt):
        try:
            response = requests.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                json={
                    "messages": [
                        {"role": "system", "content": Instruction.shellsense_ai()},
                        {"role": "user", "content": prompt},
                    ]
                },
            )
            if response.status_code == 200:
                data = response.json()
                # print(f"Full Response: {data}")  # Debug
                # Access the correct field in the response
                return data.get("result", {}).get("response", "No content returned by the API.")
            return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {e}"
