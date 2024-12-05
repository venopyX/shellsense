from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "CLOUDFLARE_ACCOUNT_ID": os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        "CLOUDFLARE_AUTH_TOKEN": os.getenv("CLOUDFLARE_AUTH_TOKEN"),
        "ACCOUNT_ID": os.getenv("ACCOUNT_ID"),
        "API_TOKEN": os.getenv("API_TOKEN"),
        "MODEL_NAME": os.getenv("MODEL_NAME"),
    }
