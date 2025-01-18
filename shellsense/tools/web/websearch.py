import logging
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class WebSearchTool(BaseTool):
    """
    A tool for searching the web using Bing and DuckDuckGo.
    Supports configurable number of results and choice of search engine.
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform web search using specified engine.

        Args:
            input_data (Dict[str, Any]): Input containing:
                - query (str): Search query
                - engine (str, optional): Search engine to use ("bing" or "ddg", default: "bing")
                - num_results (int, optional): Number of results to return (default: 5)

        Returns:
            Dict[str, Any]: Search results or error message

        Example:
            >>> tool = WebSearchTool()
            >>> results = tool.invoke({
            ...     "query": "artificial intelligence",
            ...     "engine": "bing",
            ...     "num_results": 3
            ... })
        """
        try:
            self.validate_input(input_data)
            
            query = input_data["query"]
            engine = input_data.get("engine", "bing").lower()
            num_results = min(input_data.get("num_results", 5), 10)  # Cap at 10 results
            
            logger.info(f"Searching {engine.upper()} for: {query}")
            
            if engine == "bing":
                results = self._bing_search(query, num_results)
            elif engine == "ddg":
                results = self._ddg_search(query, num_results)
            else:
                raise ValueError(f"Unsupported search engine: {engine}")
                
            if not results:
                return {"error": "No results found"}
                
            return {"results": results}
            
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return {"error": f"Invalid input: {str(e)}"}
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": f"Search request failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": f"Search failed: {str(e)}"}

    def _ddg_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Perform DuckDuckGo search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, url, and snippet
        """
        results = []
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results[:num_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    results.append({
                        'title': title_elem.text.strip(),
                        'url': title_elem['href'],
                        'snippet': snippet_elem.text.strip()
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {str(e)}")
            return []

    def _bing_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Perform Bing search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, url, and snippet
        """
        results = []
        try:
            url = f"https://www.bing.com/search?q={quote_plus(query)}&count={num_results}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.find_all('li', class_='b_algo')
            
            for result in search_results[:num_results]:
                title_elem = result.find('h2')
                link_elem = result.find('a')
                snippet_elem = result.find('div', class_='b_caption')
                
                if title_elem and link_elem and snippet_elem:
                    results.append({
                        'title': title_elem.text.strip(),
                        'url': link_elem['href'],
                        'snippet': snippet_elem.text.strip()
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"Bing search failed: {str(e)}")
            return []

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the web search tool's input parameters.

        Returns:
            Dict[str, Any]: JSON schema for validation

        Example schema:
            {
                "query": "artificial intelligence",
                "engine": "bing",
                "num_results": 5
            }
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "engine": {
                    "type": "string",
                    "description": "Search engine to use",
                    "enum": ["bing", "ddg"],
                    "default": "bing"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (max: 10)",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 5
                }
            },
            "required": ["query"]
        }
