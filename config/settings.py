import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    API_TOKEN = os.getenv("API_TOKEN")
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

# Validate the configuration
Config.validate()
