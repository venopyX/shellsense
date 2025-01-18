import logging
import requests
from typing import Dict, Any, Optional
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class GitHubTool(BaseTool):
    """
    A powerful tool for fetching publicly available information about GitHub users.
    
    This tool allows you to retrieve comprehensive details about a GitHub user by providing their username. 
    The tool will utilize this username to fetch data from the GitHub API at https://api.github.com/users/USERNAME.
    """

    def __init__(self):
        self.api_base_url = "https://api.github.com/users"

    def invoke(self, input_data: dict) -> Dict[str, Any]:
        """
        Fetch GitHub user information.

        Args:
            input_data (dict): Input dictionary containing either 'query' or 'username'.

        Returns:
            Dict[str, Any]: GitHub user data or error message.

        Raises:
            requests.RequestException: If the API request fails.
        """
        try:
            # Try both 'query' and 'username' fields
            username = input_data.get("query") or input_data.get("username")
            
            if not username:
                logger.error("No username provided")
                return {"error": "Username parameter is required."}

            logger.info(f"Fetching GitHub data for user: {username}")
            return self._fetch_github_data(username)

        except Exception as e:
            logger.error(f"Failed to process GitHub request: {str(e)}")
            return {"error": f"Failed to fetch GitHub data: {str(e)}"}

    def _fetch_github_data(self, username: str) -> Dict[str, Any]:
        """
        Make the actual API request to GitHub.

        Args:
            username (str): GitHub username to fetch data for.

        Returns:
            Dict[str, Any]: GitHub user data or error message.

        Raises:
            requests.RequestException: If the API request fails.
        """
        try:
            url = f"{self.api_base_url}/{username}"
            logger.debug(f"Making request to: {url}")
            
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            
            logger.debug("Successfully fetched GitHub data")
            return response.json()

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"GitHub user not found: {username}")
                return {"error": "GitHub user not found"}
            else:
                logger.error(f"HTTP error occurred: {str(e)}")
                return {"error": f"GitHub API error: {str(e)}"}
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": f"Failed to connect to GitHub API: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the GitHub tool's input parameters.
        
        This schema defines the expected structure of the input data for the GitHubTool. 
        The 'username' field is mandatory and should contain a single word representing 
        the GitHub username you wish to query.
        
        Returns:
            dict: JSON schema for validation and documentation.
        
        Example:
            {
                "username": "octocat"
            }
        """
        return {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "GitHub username to fetch information for (e.g., 'octocat')"
                },
                "query": {
                    "type": "string",
                    "description": "Alternative field for username (for compatibility)"
                }
            },
            "anyOf": [
                {"required": ["username"]},
                {"required": ["query"]}
            ]
        }