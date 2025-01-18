import logging
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime, timedelta
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class ProductHuntTool(BaseTool):
    """
    A tool for interacting with the ProductHunt API.
    Supports fetching posts, collections, and searching products.
    """

    def __init__(self):
        self.api_base_url = "https://api.producthunt.com/v2/api/graphql"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_TOKEN"  # TODO: Move to config
        }

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch data from ProductHunt.

        Args:
            input_data (Dict[str, Any]): Input containing:
                - action (str): Action to perform (posts, search, collection)
                - query (str, optional): Search query for search action
                - date (str, optional): Date for posts action (YYYY-MM-DD)
                - limit (int, optional): Number of results (default: 10)

        Returns:
            Dict[str, Any]: ProductHunt data or error message

        Raises:
            ValueError: If action is missing or invalid
            requests.RequestException: If the API request fails
        """
        try:
            self.validate_input(input_data)
            
            action = input_data["action"]
            limit = min(input_data.get("limit", 10), 20)  # Cap at 20
            
            logger.info(f"Fetching ProductHunt data: {action}")
            
            if action == "posts":
                date = input_data.get("date", datetime.now().strftime("%Y-%m-%d"))
                return self._get_posts(date, limit)
            elif action == "search":
                query = input_data.get("query", "")
                return self._search_products(query, limit)
            elif action == "collection":
                collection_id = input_data.get("collection_id")
                return self._get_collection(collection_id, limit)
            else:
                raise ValueError(f"Invalid action: {action}")
                
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return {"error": f"Invalid input: {str(e)}"}
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": f"Operation failed: {str(e)}"}

    def _get_posts(self, date: str, limit: int) -> Dict[str, Any]:
        """
        Get posts for a specific date.

        Args:
            date (str): Date in YYYY-MM-DD format
            limit (int): Number of results to return

        Returns:
            Dict[str, Any]: Posts data
        """
        query = """
        query Posts($date: Date!, $limit: Int!) {
            posts(first: $limit, postedAfter: $date) {
                edges {
                    node {
                        id
                        name
                        tagline
                        description
                        url
                        votesCount
                        website
                        thumbnail {
                            url
                        }
                    }
                }
            }
        }
        """
        
        variables = {"date": date, "limit": limit}
        return self._execute_query(query, variables)

    def _search_products(self, query: str, limit: int) -> Dict[str, Any]:
        """
        Search for products.

        Args:
            query (str): Search query
            limit (int): Number of results to return

        Returns:
            Dict[str, Any]: Search results
        """
        query_str = """
        query Search($query: String!, $limit: Int!) {
            search(first: $limit, query: $query) {
                edges {
                    node {
                        id
                        name
                        tagline
                        description
                        url
                        votesCount
                    }
                }
            }
        }
        """
        
        variables = {"query": query, "limit": limit}
        return self._execute_query(query_str, variables)

    def _get_collection(self, collection_id: str, limit: int) -> Dict[str, Any]:
        """
        Get collection details.

        Args:
            collection_id (str): Collection ID
            limit (int): Number of results to return

        Returns:
            Dict[str, Any]: Collection data
        """
        query = """
        query Collection($id: ID!, $limit: Int!) {
            collection(id: $id) {
                id
                name
                description
                posts(first: $limit) {
                    edges {
                        node {
                            id
                            name
                            tagline
                            url
                            votesCount
                        }
                    }
                }
            }
        }
        """
        
        variables = {"id": collection_id, "limit": limit}
        return self._execute_query(query, variables)

    def _execute_query(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a GraphQL query.

        Args:
            query (str): GraphQL query
            variables (Dict[str, Any]): Query variables

        Returns:
            Dict[str, Any]: Query results

        Raises:
            requests.RequestException: If the request fails
        """
        try:
            response = requests.post(
                self.api_base_url,
                headers=self.headers,
                json={"query": query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                raise ValueError(str(data["errors"]))
                
            return data["data"]
            
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the ProductHunt tool's input parameters.

        Returns:
            Dict[str, Any]: JSON schema for validation and documentation.

        Example:
            {
                "action": "posts",
                "date": "2024-01-19",
                "limit": 10
            }
        """
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["posts", "search", "collection"]
                },
                "query": {
                    "type": "string",
                    "description": "Search query (required for search action)"
                },
                "date": {
                    "type": "string",
                    "description": "Date for posts action (YYYY-MM-DD format)"
                },
                "collection_id": {
                    "type": "string",
                    "description": "Collection ID (required for collection action)"
                },
                "limit": {
                    "type": "number",
                    "description": "Number of results to return (default: 10, max: 20)",
                    "minimum": 1,
                    "maximum": 20
                }
            },
            "required": ["action"]
        }
