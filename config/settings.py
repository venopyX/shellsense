import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    API_TOKEN = os.getenv("CLOUDFLARE_AUTH_TOKEN")

    FUNCTION_CALL_MODEL = os.getenv("FUNCTION_CALL_MODEL", "@hf/nousresearch/hermes-2-pro-mistral-7b")
    FRIENDLY_RESPONSE_MODEL = os.getenv("FRIENDLY_RESPONSE_MODEL", "@hf/mistral/mistral-7b-instruct-v0.2")

    CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{FUNCTION_CALL_MODEL}"

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY or not Config.ACCOUNT_ID or not Config.API_TOKEN:
            raise EnvironmentError("Required environment variables are missing.")
