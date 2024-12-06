from openai import OpenAI
from config.settings import Config
from pyplugin.utils.instruction import Instruction


class OpenAIProvider:
    def __init__(self):
        Config.validate()
        self.API_KEY = Config.OPENAI_API_KEY
        self.client = OpenAI()

    def chat(self, prompt):
        try:
            self.client.api_key = self.API_KEY
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": Instruction.shellsense_ai()},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"Error: {e}"


class CloudflareProvider:
    def __init__(self):
        Config.validate()
        self.account_id = Config.ACCOUNT_ID
        self.auth_token = Config.API_TOKEN
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
                return data.get("result", {}).get("response", "No content returned by the API.")
            return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {e}"
