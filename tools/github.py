# tools/github.py

import requests
from tools.base_tool import BaseTool

class GitHubTool(BaseTool):
    """
    A powerful tool for fetching publicly available information about GitHub users by taking username as parameter.
    
    This tool allows you to retrieve comprehensive details about a GitHub user by providing their username. 
    The tool will utilize this username to fetch data from the GitHub API at https://api.github.com/users/USERNAME
    """

    def invoke(self, input: dict) -> dict:
        username = input.get("query")
        if not username:
            username = input.get("username")
            if not username:
                return {"error": "Username parameter is required."}

        try:
            response = requests.get(f"https://api.github.com/users/{username}")
            if response.status_code == 200:
                return response.json()
            return {"error": f"GitHub user not found, status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"Exception fetching GitHub user data: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the GitHub tool's input parameters.
        
        This schema defines the expected structure of the input data for the GitHubTool. 
        The 'username' field is mandatory and should contain a single word representing 
        the GitHub username you wish to query. The tool will utilize this username to 
        fetch data from the GitHub API at https://api.github.com/users/USERNAME.
        
        Example usage: 
        {
            "username": "david123"
        }
        """
        return {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": (
                        "The GitHub username to fetch information for (single word)."
                        "Ensure to provide only the username value (e.g., 'username1') for accurate results."
                    )
                }
            },
            "required": ["username"]
        }