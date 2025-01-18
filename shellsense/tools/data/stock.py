import logging
from typing import Dict, Any, Optional, List
import yfinance as yf
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class StockTool(BaseTool):
    """
    Provides stock analysis tools, including fetching current prices, company profiles, and analyst recommendations.
    """

    def invoke(self, input_data: dict) -> Dict[str, Any]:
        """
        Process stock-related requests.

        Args:
            input_data (dict): Input containing:
                - action (str): The action to perform (getCurrentPrice, getCompanyProfile, getAnalystRecommendations)
                - symbol (str): The stock symbol to analyze

        Returns:
            Dict[str, Any]: Stock data or error message based on the requested action

        Raises:
            ValueError: If required parameters are missing
            yfinance.exceptions.YFinanceError: If there's an error fetching stock data
        """
        try:
            action: str = input_data.get("action", "")
            symbol: str = input_data.get("symbol", "")
            
            if not symbol or not action:
                logger.error("Missing required parameters")
                return {"error": "Both 'symbol' and 'action' parameters are required."}

            logger.info(f"Processing {action} request for symbol: {symbol}")
            return self._process_stock_action(action, symbol)

        except Exception as e:
            logger.error(f"Failed to process stock request: {str(e)}")
            return {"error": f"Stock data retrieval failed: {str(e)}"}

    def _process_stock_action(self, action: str, symbol: str) -> Dict[str, Any]:
        """
        Process a specific stock action.

        Args:
            action (str): The action to perform
            symbol (str): The stock symbol

        Returns:
            Dict[str, Any]: Stock data or error message
        """
        try:
            stock = yf.Ticker(symbol)
            
            actions = {
                "getCurrentPrice": lambda: self._get_current_price(stock),
                "getCompanyProfile": lambda: self._get_company_profile(stock),
                "getAnalystRecommendations": lambda: self._get_analyst_recommendations(stock)
            }
            
            if action not in actions:
                logger.error(f"Invalid action requested: {action}")
                return {"error": "Invalid action specified."}
                
            return actions[action]()

        except Exception as e:
            logger.error(f"Error processing {action} for {symbol}: {str(e)}")
            return {"error": f"Failed to process {action}: {str(e)}"}

    def _get_current_price(self, stock: yf.Ticker) -> Dict[str, Any]:
        """Get current stock price."""
        try:
            price = stock.info.get("regularMarketPrice")
            if price is None:
                logger.warning("Current price data not available")
                return {"error": "Current price data is not available."}
            
            logger.debug(f"Successfully retrieved current price: {price}")
            return {"price": price}
        except Exception as e:
            logger.error(f"Failed to get current price: {str(e)}")
            return {"error": f"Failed to get current price: {str(e)}"}

    def _get_company_profile(self, stock: yf.Ticker) -> Dict[str, Any]:
        """Get company profile information."""
        try:
            profile = {
                "name": stock.info.get("longName"),
                "sector": stock.info.get("sector"),
                "industry": stock.info.get("industry"),
                "description": stock.info.get("longBusinessSummary"),
            }
            # Filter out None values
            profile = {k: v for k, v in profile.items() if v is not None}
            
            if not profile:
                logger.warning("Company profile data not available")
                return {"error": "Company profile data is not available."}
                
            logger.debug("Successfully retrieved company profile")
            return profile
        except Exception as e:
            logger.error(f"Failed to get company profile: {str(e)}")
            return {"error": f"Failed to get company profile: {str(e)}"}

    def _get_analyst_recommendations(self, stock: yf.Ticker) -> Dict[str, Any]:
        """Get analyst recommendations."""
        try:
            recommendations = stock.recommendations
            if recommendations is None or recommendations.empty:
                logger.warning("No analyst recommendations available")
                return {"recommendations": []}
                
            logger.debug("Successfully retrieved analyst recommendations")
            return {"recommendations": recommendations.to_dict("records")}
        except Exception as e:
            logger.error(f"Failed to get analyst recommendations: {str(e)}")
            return {"error": f"Failed to get analyst recommendations: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the stock tool's input parameters.

        Returns:
            dict: JSON schema for validation and documentation.

        Example:
            {
                "symbol": "AAPL",
                "action": "getCurrentPrice"
            }
        """
        return {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g., AAPL, GOOGL)"
                },
                "action": {
                    "type": "string",
                    "enum": ["getCurrentPrice", "getCompanyProfile", "getAnalystRecommendations"],
                    "description": "Action to perform on the stock data"
                }
            },
            "required": ["symbol", "action"]
        }