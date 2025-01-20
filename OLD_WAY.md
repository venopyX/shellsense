Directory Structure:

└── ./
    ├── tools
    │   ├── __init__.py
    │   ├── github.py
    │   ├── stock.py
    │   └── tool_manager.py
    ├── config.py
    └── main.py



---
File: /tools/__init__.py
---




---
File: /tools/github.py
---

import requests
from langchain.tools import tool

@tool
def get_github_user(username: str) -> dict:
    """Fetches publicly available information about a GitHub user."""
    try:
        github_response = requests.get(f"https://api.github.com/users/{username}")
        if github_response.status_code == 200:
            return github_response.json()
        else:
            return {"error": f"GitHub user not found, status code: {github_response.status_code}"}
    except Exception as e:
        return {"error": f"Exception fetching GitHub user data: {e}"}



---
File: /tools/stock.py
---

import yfinance as yf
from langchain.tools import tool

@tool
def get_current_stock_price(symbol: str) -> float:
    """Get the current stock price for a given symbol."""
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.info.get("regularMarketPrice", stock.info.get("currentPrice"))
        return current_price if current_price else None
    except Exception as e:
        print(f"Error fetching current price for {symbol}: {e}")
        return None

@tool
def get_company_profile(symbol: str) -> dict:
    """Get the company profile for a given symbol."""
    try:
        stock = yf.Ticker(symbol)
        profile = {
            "name": stock.info.get("longName"),
            "sector": stock.info.get("sector"),
            "industry": stock.info.get("industry"),
            "description": stock.info.get("longBusinessSummary"),
        }
        return profile
    except Exception as e:
        print(f"Error fetching profile for {symbol}: {e}")
        return {}

@tool
def get_analyst_recommendations(symbol: str) -> list:
    """Get analyst recommendations for a given stock symbol."""
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations.to_dict("records") if stock.recommendations is not None else []
        return recommendations
    except Exception as e:
        print(f"Error fetching recommendations for {symbol}: {e}")
        return []



---
File: /tools/tool_manager.py
---

import requests
from .github import get_github_user
from .stock import (
    get_current_stock_price,
    get_company_profile,
    get_analyst_recommendations,
)

class ToolManager:
    def __init__(self, account_id, api_token):
        self.account_id = account_id
        self.api_token = api_token
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@hf/nousresearch/hermes-2-pro-mistral-7b"
        self.tool_mapping = {
            "getGithubUser": get_github_user,
            "getCurrentStockPrice": get_current_stock_price,
            "getCompanyProfile": get_company_profile,
            "getAnalystRecommendations": get_analyst_recommendations,
        }
        self.tools = self.prepare_tools()

    def prepare_tools(self):
        return [
            {
                "name": "getGithubUser",
                "description": "Fetches publicly available information about a GitHub user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "The GitHub username."
                        }
                    },
                    "required": ["username"]
                },
            },
            {
                "name": "getCurrentStockPrice",
                "description": "Get the current stock price for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol."
                        }
                    },
                    "required": ["symbol"]
                },
            },
            {
                "name": "getCompanyProfile",
                "description": "Get the company profile for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol."
                        }
                    },
                    "required": ["symbol"]
                },
            },
            {
                "name": "getAnalystRecommendations",
                "description": "Get analyst recommendations for a given stock symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol."
                        }
                    },
                    "required": ["symbol"]
                },
            },
        ]

    def process_query(self, user_query):
        payload = {
            "messages": [{"role": "user", "content": user_query}],
            "tools": self.tools,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

        response = requests.post(self.url, json=payload, headers=headers)
        print("Cloudflare API Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            tool_calls = data.get("result", {}).get("tool_calls", [])

            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments", {})
                result = self.call_tool(tool_name, arguments)
                print(f"Result from {tool_name}: {result}")
        else:
            print("Error calling Cloudflare API:", response.status_code, response.text)

    def call_tool(self, tool_name, arguments):
        """
        Dynamically call a tool function based on the tool name.

        Args:
            tool_name (str): Name of the tool to call.
            arguments (dict): Arguments to pass to the tool.

        Returns:
            Result from the tool function or an error message.
        """
        func = self.tool_mapping.get(tool_name)
        if func:
            return func.invoke(input=arguments)
        return {"error": f"Tool '{tool_name}' not found."}



---
File: /config.py
---

import os
from dotenv import load_dotenv

load_dotenv()

account_id = os.getenv("ACCOUNT_ID")
api_token = os.getenv("API_TOKEN")

model_name = os.getenv("MODEL_NAME")
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}"



---
File: /main.py
---

from config import account_id, api_token, url
from tools.tool_manager import ToolManager

def main():
    user_query = input("Enter your question: ")
    tool_manager = ToolManager(account_id, api_token)
    tool_manager.process_query(user_query)

if __name__ == "__main__":
    main()

