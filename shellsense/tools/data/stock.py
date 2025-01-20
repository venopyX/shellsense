import yfinance as yf

from shellsense.tools.base_tool import BaseTool


class StockTool(BaseTool):
    """
    Retrieves stock data including current prices, company profiles, and analyst recommendations.

    Args:
        action (str): The action to perform (e.g., 'getCurrentPrice', 'getCompanyProfile', or 'getAnalystRecommendations').
        symbol (str): The stock symbol to fetch data for.
    """

    def invoke(self, input: dict) -> dict:
        action: str = input.get("action")
        symbol: str = input.get("symbol")

        if not symbol or not action:
            return {"error": "Both 'symbol' and 'action' are required."}

        try:
            stock = yf.Ticker(symbol)
            if action == "getCurrentPrice":
                price = stock.info.get("regularMarketPrice")
                if price is None:
                    return {"error": "Current price data is unavailable."}
                return {"price": price}

            elif action == "getCompanyProfile":
                profile = {
                    "name": stock.info.get("longName"),
                    "sector": stock.info.get("sector"),
                    "industry": stock.info.get("industry"),
                    "description": stock.info.get("longBusinessSummary"),
                }
                profile = {k: v for k, v in profile.items() if v is not None}
                return (
                    profile
                    if profile
                    else {"error": "Company profile data is unavailable."}
                )

            elif action == "getAnalystRecommendations":
                recommendations = (
                    stock.recommendations.to_dict("records")
                    if stock.recommendations
                    else []
                )
                return {"recommendations": recommendations}

            else:
                return {"error": "Invalid action specified."}

        except Exception as e:
            return {"error": f"Error retrieving stock data: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the stock tool's input parameters.

        Returns:
            dict: JSON schema for the stock tool input.
        """
        return {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "The stock symbol."},
                "action": {
                    "type": "string",
                    "description": "Action to perform ('getCurrentPrice', 'getCompanyProfile', 'getAnalystRecommendations').",
                    "enum": [
                        "getCurrentPrice",
                        "getCompanyProfile",
                        "getAnalystRecommendations",
                    ],
                },
            },
            "required": ["symbol", "action"],
        }
