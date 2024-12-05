# tools/stock.py

import yfinance as yf
from tools.base_tool import BaseTool

class StockTool(BaseTool):
    """
    Provides stock analysis tools, including fetching current prices, company profiles, and analyst recommendations.
    """

    def invoke(self, input: dict) -> dict:
        action = input.get("action")
        symbol = input.get("symbol")
        if not symbol or not action:
            return {"error": "Both 'symbol' and 'action' parameters are required."}

        try:
            stock = yf.Ticker(symbol)
            if action == "getCurrentPrice":
                return {"price": stock.info.get("regularMarketPrice")}
            elif action == "getCompanyProfile":
                return {
                    "name": stock.info.get("longName"),
                    "sector": stock.info.get("sector"),
                    "industry": stock.info.get("industry"),
                    "description": stock.info.get("longBusinessSummary"),
                }
            elif action == "getAnalystRecommendations":
                recommendations = stock.recommendations.to_dict("records") if stock.recommendations is not None else []
                return {"recommendations": recommendations}
            else:
                return {"error": "Invalid action specified."}
        except Exception as e:
            return {"error": f"Exception during stock data retrieval: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the stock tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to fetch data for."
                },
                "action": {
                    "type": "string",
                    "description": "Action to perform: 'getCurrentPrice', 'getCompanyProfile', or 'getAnalystRecommendations'.",
                    "enum": ["getCurrentPrice", "getCompanyProfile", "getAnalystRecommendations"]
                }
            },
            "required": ["symbol", "action"]
        }
