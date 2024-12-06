import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID") or os.getenv("CLOUDFLARE_ACCOUNT_ID")
    API_TOKEN = os.getenv("API_TOKEN") or os.getenv("CLOUDFLARE_AUTH_TOKEN")
    MODEL_NAME = os.getenv("MODEL_NAME")
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"
    CLOUDFLARE_API_URL = (
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL_NAME}"
    )

    @staticmethod
    def validate():
        if not Config.ACCOUNT_ID or not Config.API_TOKEN or not Config.MODEL_NAME:
            raise ValueError(
                "Please ensure ACCOUNT_ID, API_TOKEN, and MODEL_NAME are set in the .env file."
            )


Config.validate()
